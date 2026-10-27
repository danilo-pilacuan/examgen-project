$ErrorActionPreference = 'Continue'
$base = 'http://localhost:8000'

# Login both users
$lA = Invoke-RestMethod -Uri "$base/auth/login" -Method Post -ContentType 'application/json' -Body '{"email":"qa-r8-a@usfq.test","password":"Qa-R8-Pass-2026!"}'
$lB = Invoke-RestMethod -Uri "$base/auth/login" -Method Post -ContentType 'application/json' -Body '{"email":"qa-r8-b@usfq.test","password":"Qa-R8-Pass-2026!"}'
$tokA = $lA.access_token
$tokB = $lB.access_token
Write-Output "1. login A ok ($($lA.user.id)), login B ok ($($lB.user.id))"

# Initial lists (both empty)
$la = Invoke-RestMethod -Uri "$base/api/chat/threads" -Headers @{Authorization="Bearer $tokA"}
$lb = Invoke-RestMethod -Uri "$base/api/chat/threads" -Headers @{Authorization="Bearer $tokB"}
Write-Output "2. initial lists: A=$($la.Count) threads, B=$($lb.Count) threads"

# A sends a first turn (registers thread with pinned title)
$tid = [guid]::NewGuid().ToString()
$script:tidA = $tid
$body = @{ message = 'Hola: conversacion de control QA ronda 8'; thread_id = $tid } | ConvertTo-Json
try {
  $r = Invoke-RestMethod -Uri "$base/api/chat" -Method Post -ContentType 'application/json' -Headers @{Authorization="Bearer $tokA"} -Body $body -TimeoutSec 240
  Write-Output "3. A first turn ok (thread $tid)"
} catch {
  Write-Output "3. A first turn FAILED: $($_.Exception.Message) $($_.ErrorDetails.Message)"
  exit 1
}

# List after first turn: badges present, title pinned
$la = Invoke-RestMethod -Uri "$base/api/chat/threads" -Headers @{Authorization="Bearer $tokA"}
$thread = $la | Where-Object { $_.thread_id -eq $tid }
Write-Output "4. A list now $($la.Count) thread(s); title='$($thread.title)'; last_subject_name='$($thread.last_subject_name)'; message_count=$($thread.message_count)"

# B's list must NOT contain A's thread (BUG-022 fix)
$lb = Invoke-RestMethod -Uri "$base/api/chat/threads" -Headers @{Authorization="Bearer $tokB"}
$leak = $lb | Where-Object { $_.thread_id -eq $tid }
Write-Output "5. B list has $($lb.Count) thread(s); A thread leaked to B: $([bool]$leak)"

# B tries to read A's history -> 403
try {
  Invoke-RestMethod -Uri "$base/api/chat/history/$tid" -Headers @{Authorization="Bearer $tokB"} | Out-Null
  Write-Output "6. B read A history: NO 403 (FAIL)"
} catch {
  Write-Output "6. B read A history -> HTTP $($_.Exception.Response.StatusCode.value__) (expect 403)"
}

# B tries to write into A's thread -> 403
$bodyB = @{ message = 'intrusion'; thread_id = $tid } | ConvertTo-Json
try {
  Invoke-RestMethod -Uri "$base/api/chat" -Method Post -ContentType 'application/json' -Headers @{Authorization="Bearer $tokB"} -Body $bodyB -TimeoutSec 60 | Out-Null
  Write-Output "7. B wrote into A thread: NO 403 (FAIL)"
} catch {
  Write-Output "7. B write into A thread -> HTTP $($_.Exception.Response.StatusCode.value__) (expect 403)"
}

# B renames A's thread -> 403
try {
  Invoke-RestMethod -Uri "$base/api/chat/threads/$tid" -Method Patch -ContentType 'application/json' -Headers @{Authorization="Bearer $tokB"} -Body '{"title":"hacked"}' | Out-Null
  Write-Output "8. B renamed A thread: NO 403 (FAIL)"
} catch {
  Write-Output "8. B rename A thread -> HTTP $($_.Exception.Response.StatusCode.value__) (expect 403)"
}

# B deletes A's thread -> 403
try {
  Invoke-RestMethod -Uri "$base/api/chat/threads/$tid" -Method Delete -Headers @{Authorization="Bearer $tokB"} | Out-Null
  Write-Output "9. B deleted A thread: NO 403 (FAIL)"
} catch {
  Write-Output "9. B delete A thread -> HTTP $($_.Exception.Response.StatusCode.value__) (expect 403)"
}

# A second turn: title stays pinned, message_count grows
$body2 = @{ message = 'Segundo turno de control, el titulo no debe cambiar'; thread_id = $tid } | ConvertTo-Json
try {
  Invoke-RestMethod -Uri "$base/api/chat" -Method Post -ContentType 'application/json' -Headers @{Authorization="Bearer $tokA"} -Body $body2 -TimeoutSec 240 | Out-Null
  $la = Invoke-RestMethod -Uri "$base/api/chat/threads" -Headers @{Authorization="Bearer $tokA"}
  $t2 = $la | Where-Object { $_.thread_id -eq $tid }
  Write-Output "10. after 2nd turn: title='$($t2.title)' (pinned, must not change); message_count=$($t2.message_count) (expect 4)"
} catch {
  Write-Output "10. A 2nd turn FAILED: $($_.Exception.Message)"
}

# A renames own thread -> 200
try {
  Invoke-RestMethod -Uri "$base/api/chat/threads/$tid" -Method Patch -ContentType 'application/json' -Headers @{Authorization="Bearer $tokA"} -Body '{"title":"Titulo editado por dueno"}' | Out-Null
  $la = Invoke-RestMethod -Uri "$base/api/chat/threads" -Headers @{Authorization="Bearer $tokA"}
  $t3 = $la | Where-Object { $_.thread_id -eq $tid }
  Write-Output "11. A renamed own thread -> 200, new title='$($t3.title)'"
} catch {
  Write-Output "11. A rename FAILED: HTTP $($_.Exception.Response.StatusCode.value__)"
}

# A deletes own thread -> 204 then list is empty
try {
  Invoke-RestMethod -Uri "$base/api/chat/threads/$tid" -Method Delete -Headers @{Authorization="Bearer $tokA"} | Out-Null
  $la = Invoke-RestMethod -Uri "$base/api/chat/threads" -Headers @{Authorization="Bearer $tokA"}
  Write-Output "12. A deleted own thread -> 200/204; A list count now $($la.Count)"
} catch {
  Write-Output "12. A delete FAILED: HTTP $($_.Exception.Response.StatusCode.value__)"
}

# Cloud Fallback (Rare Cases Only)

Almost everyone should be able to complete this workshop on their own laptop by following
[README.md](README.md). This page is only for the rare situation where a laptop genuinely
can't run Ollama — for example:

- Very old hardware with less than ~8 GB of RAM or very little free disk space
- A locked-down corporate/school laptop that blocks installing new software entirely
- An unsupported OS/architecture

## What to do

**This is not a self-service option.** Setting it up requires an AWS account, which most
freshmen won't have, and it costs a small amount of real money to run. If you hit a wall
where your laptop truly can't run Ollama:

1. Raise your hand and talk to the instructor first — most "can't install" problems have a
   simpler fix (see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)), and pairing up with a
   neighbor to watch/follow along is often enough to still get the learning value even if
   you can't run it yourself that day.
2. If the instructor decides a cloud fallback is warranted, **they** will spin up a
   temporary cloud machine for you to SSH into (using the same
   [`aws/template.yaml`](../aws/template.yaml) CloudFormation template used for the
   instructor's own demo), share short-lived SSH access, and walk you through running
   `ollama pull` and `chat.py` on that machine instead of your own laptop.
3. Once you're done, the instructor will tear down that machine — you won't need to manage
   any AWS resources yourself.

## Why it's instructor-operated, not self-service

- It requires an AWS account with billing set up, which most students don't have and
  shouldn't need to create just for this workshop.
- Every running cloud instance costs money for as long as it's up, even if idle — having
  the instructor manage a single shared fallback machine (or spin up one per affected
  student, torn down right after) keeps this controlled and cheap, versus students
  potentially forgetting to shut down cloud resources they set up in a hurry.
- SSH access to a fallback machine still needs a properly restricted security group
  (limited to specific IPs) — something the instructor's existing template already handles
  correctly.

If you're the instructor reading this while prepping: this fallback re-uses the exact same
`aws/template.yaml` from your own demo setup. See [`aws/DEMO-STEPS.md`](../aws/DEMO-STEPS.md)
for the deploy/SSH/teardown commands — for a student fallback, just deploy a second stack
(with a different `--stack-name`) so it doesn't collide with your own demo instance, and
delete it as soon as that student is done.

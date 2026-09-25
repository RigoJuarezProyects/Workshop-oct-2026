# Instructor Live-Demo Checklist

This is your own script for the 5-10 minute live terminal demo at the start of the workshop.
Rehearse this at least once end-to-end before the real session (see timing notes at the
bottom).

## Before the workshop (do this the night before or morning of)

1. Find your current public IP (for the SSH security group rule):
   ```bash
   curl -s https://checkip.amazonaws.com
   ```

2. Deploy the stack (replace `my-key` with your EC2 key pair name). **Don't retype the IP
   from step 1 by hand** — capture it into a variable and reuse it, to avoid typos like an
   extra digit sneaking into the CIDR (this has bitten people before and causes SSH to hang
   silently instead of failing loudly — see [Troubleshooting](#troubleshooting) below):
   ```bash
   MY_IP=$(curl -s https://checkip.amazonaws.com)
   echo "Using CIDR: ${MY_IP}/32"   # double check this looks like a real IP before continuing

   aws cloudformation deploy \
     --template-file aws/template.yaml \
     --stack-name llm-workshop-demo \
     --parameter-overrides \
       KeyPairName=my-key \
       SSHLocationCIDR=${MY_IP}/32 \
     --capabilities CAPABILITY_IAM
   ```

3. Get the instance's public IP and SSH command from the stack outputs:
   ```bash
   aws cloudformation describe-stacks \
     --stack-name llm-workshop-demo \
     --query "Stacks[0].Outputs"
   ```

4. SSH in (using the IP from the previous step):
   ```bash
   ssh -i /path/to/my-key.pem ubuntu@<InstancePublicIP>
   ```

5. Install Ollama on the instance:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama --version
   ```

6. Pre-pull both models **now**, not during class, so the live demo doesn't wait on a
   download:
   ```bash
   ollama pull llama3.2
   ollama pull qwen2.5:3b
   ollama list
   ```
   > **Note:** use `qwen2.5:3b` explicitly, not just `qwen2.5` — the bare tag resolves to
   > the much larger 7B model (~4.7GB), which can exceed available RAM and cause Ollama to
   > crash (`server disconnected without sending a response`) when switching between models
   > mid-session on smaller instances.

7. If you also want to test/demo the actual `chat.py` script (not just `ollama run`
   directly) on this instance, clone the repo and set up the Python environment. Ubuntu's
   `python3-venv` package isn't installed by default, and the package index on a fresh
   instance is often stale, so update it first:
   ```bash
   sudo apt update
   sudo apt install -y python3-venv

   git clone https://github.com/<your-org>/llm-workshop.git
   cd llm-workshop
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

   python3 chat.py
   ```
   > If `sudo apt install python3-venv` still reports "no installation candidate", it means
   > `sudo apt update` didn't run first (or failed) — the AMI's package index is stale until
   > you refresh it. Re-run `sudo apt update`, then retry the install.

8. Do one full rehearsal run of the "During the workshop" steps below, and disconnect
   (`exit` from SSH) when done. Leave the stack running if the workshop is soon, or delete it
   and redeploy on the day (see Teardown below) — either is fine, cost is negligible either
   way (see `EstimatedHourlyCost` output).

## During the workshop (the actual 5-10 minute live demo)

SSH into the instance again (screen-share this terminal):

```bash
ssh -i /path/to/my-key.pem ubuntu@<InstancePublicIP>
```

Then, live, in front of the class:

1. Show the models are already there:
   ```bash
   ollama list
   ```

2. Run a single demo prompt with `llama3.2` (pick something fun/relatable for freshmen):
   ```bash
   ollama run llama3.2 "Explain what a large language model is, in two sentences, for a first-year CS student."
   ```

3. (Optional, if time allows) Run the same prompt with `qwen2.5:3b` to show the contrast:
   ```bash
   ollama run qwen2.5:3b "Explain what a large language model is, in two sentences, for a first-year CS student."
   ```

4. Explain: "this is exactly what you're about to do on your own laptop — the only
   difference is you'll use a small Python script instead of the `ollama run` command
   directly."

That's it — keep it short, this is just to show the expected end-state before students start
their own setup.

## After the workshop: tear down

**Important — this deletes the EC2 instance and its EBS volume.** Do this once you're done
with the demo for the day, to stop paying for the instance (it's cheap, but no reason to
leave it running).

```bash
aws cloudformation delete-stack --stack-name llm-workshop-demo
aws cloudformation wait stack-delete-complete --stack-name llm-workshop-demo
```

Confirm no resources are left in the EC2/EBS console for this stack afterward.

## Timing notes

- Full rehearsal (steps 1-4 of "During the workshop", starting from an already-running,
  pre-pulled instance) should take well under 5 minutes — if your rehearsal runs longer,
  trim to just step 2 (one model, one prompt) for the actual live demo.
- Steps 1-6 of "Before the workshop" (deploy through pre-pulling models) typically take
  10-15 minutes total and should be done well ahead of class time, not while students are
  waiting. Step 7 (optional `chat.py` setup on the instance) adds a couple more minutes if
  you use it.

## Troubleshooting

### SSH just hangs forever (no connection, no error)

This almost always means the security group doesn't actually allow your current IP —
packets to port 22 get silently dropped rather than actively refused, so `ssh` just hangs
instead of failing with a clear error. Common causes:

- **Typo in the CIDR** when it was typed by hand (e.g. an extra digit, like `235.x.x.x`
  instead of `35.x.x.x`). Always capture your IP into a variable and echo it before using it
  (see step 2 above) instead of retyping it.
- **Your IP changed** since you deployed — common if you're on a VPN, corporate network, or
  switched wifi networks. Re-check with `curl -s https://checkip.amazonaws.com` and compare
  to what's actually allowed (see below).

To check what's actually allowed and fix it without a full redeploy:

```bash
# Find the real security group ID (the "PhysicalResourceId" here is a
# generated name, not a sg-xxxx ID — look it up by that name to get the ID):
aws cloudformation list-stack-resources --stack-name llm-workshop-demo --region us-east-1

aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=<name-from-above>" \
  --region us-east-1 \
  --query "SecurityGroups[0].{GroupId:GroupId,Rules:IpPermissions}"

# Confirm your current IP:
curl -s https://checkip.amazonaws.com

# If it doesn't match the CIDR shown above, fix it directly (faster than a
# redeploy) — replace <sg-id> and <wrong-cidr>/<correct-ip> accordingly:
aws ec2 revoke-security-group-ingress \
  --group-id <sg-id> --protocol tcp --port 22 --cidr <wrong-cidr>/32 --region us-east-1

aws ec2 authorize-security-group-ingress \
  --group-id <sg-id> --protocol tcp --port 22 --cidr <your-current-ip>/32 --region us-east-1
```

Then retry the SSH command — it should connect immediately.

### `Invalid security group description` on deploy

AWS security group descriptions only allow a specific character set
(`a-zA-Z0-9. _-:/()#,@[]+=&;{}!$*`) — notably **no apostrophes**. If you edit the template
and add a description with an apostrophe (e.g. "instructor's IP"), the stack will fail to
create. Use plain text without punctuation like apostrophes in `GroupDescription` fields.

### `ensurepip is not available` / `python3-venv` has no installation candidate

If `python3 -m venv .venv` fails with a message about `ensurepip` or missing
`python3.10-venv`, and `sudo apt install python3.10-venv` reports "no installation
candidate", the instance's apt package index is stale (common on a freshly launched AMI).
Refresh it first, and install the generic `python3-venv` meta-package rather than a
version-pinned one:

```bash
sudo apt update
sudo apt install -y python3-venv
```

Then retry `python3 -m venv .venv`.

### `[Unexpected error: Server disconnected without sending a response.]` when switching models

This means Ollama's `llama-server` process was killed by the OS out-of-memory (OOM)
killer — check with `sudo dmesg | tail -30` and look for a line mentioning `oom-kill` or
`Out of memory: Killed process ... llama-server`. This happens when two models are loaded in
memory at the same time and their combined size exceeds available RAM.

The most common cause is pulling `qwen2.5` **without** the `:3b` tag — the bare `qwen2.5`
tag resolves to the 7B model (~4.7GB weights, ~5GB+ resident in memory), not the 3B one
(~1.9GB). Running `llama3.2` (3B, ~2GB resident) and `qwen2.5` (7B, ~5GB resident)
simultaneously can exceed the RAM on a `t4g.large`/`t4g.medium` instance (or a laptop with
8GB total RAM).

Fix: remove the wrong model and re-pull with the explicit 3B tag:
```bash
ollama rm qwen2.5
ollama pull qwen2.5:3b
```
Then make sure `chat.py` and any other scripts reference `qwen2.5:3b`, not bare `qwen2.5`
(the version of `chat.py` in this repo already does this correctly).

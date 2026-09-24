# Instructor Live-Demo Checklist

This is your own script for the 5-10 minute live terminal demo at the start of the workshop.
Rehearse this at least once end-to-end before the real session (see timing notes at the
bottom).

## Before the workshop (do this the night before or morning of)

1. Find your current public IP (for the SSH security group rule):
   ```bash
   curl -s https://checkip.amazonaws.com
   ```

2. Deploy the stack (replace `my-key` with your EC2 key pair name, and the CIDR with
   `<your-ip>/32`):
   ```bash
   aws cloudformation deploy \
     --template-file aws/template.yaml \
     --stack-name llm-workshop-demo \
     --parameter-overrides \
       KeyPairName=my-key \
       SSHLocationCIDR=203.0.113.5/32 \
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
   ollama pull qwen2.5
   ollama list
   ```

7. Do one full rehearsal run of the "During the workshop" steps below, and disconnect
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

3. (Optional, if time allows) Run the same prompt with `qwen2.5` to show the contrast:
   ```bash
   ollama run qwen2.5 "Explain what a large language model is, in two sentences, for a first-year CS student."
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
  waiting.

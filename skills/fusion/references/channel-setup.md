# Claude Channel Setup

Use this reference when the fusion loop cannot find a reachable Claude Code channel.

Source of truth: `aaronn/claude-channel-cli` publishes the `claude-channel` CLI. As of v0.2.0 it requires Node 22 or newer.

## Diagnose

Run these checks from Codex or a shell:

```sh
node --version
command -v claude-channel
claude-channel --version
claude-channel list
claude-channel status
```

Interpretation:

- `command -v claude-channel` returns nothing: the CLI is not installed or is not on `PATH`.
- `claude-channel status` cannot find a target: Claude Code is not running with the channel enabled for this project.
- Multiple targets appear: ask the user which visible Claude Code window to use.

## Install CLI

Tell the user to install the CLI once:

```sh
npm install -g claude-channel-cli
```

If Node is older than 22, tell the user to switch or install Node 22+ before retrying.

## Register Receiver Project

In the project where Claude Code should receive fusion prompts, tell the user to run:

```sh
cd /path/to/project
claude-channel setup-mcp
```

This registers the receiver-side MCP server so the CLI can identify the correct Claude Code session when more than one is open.

## Start Claude Code In Another Tab

Tell the user to open another terminal tab in the same project and run:

```sh
cd /path/to/project
claude --dangerously-load-development-channels server:claude-channel-cli
```

Claude Code currently shows a warning for development channels. Tell the user to choose:

```text
1. I am using this for local development
```

Keep that Claude Code tab open. It is the receiver session.

## Register Codex Plugin

If Codex does not have typed Claude Channel tools, tell the user to run:

```sh
claude-channel setup-codex-plugin
codex plugin add claude-channel-cli@personal
```

Then start a new Codex thread so the plugin tools are discoverable.

## Confirm Ready

After the user completes setup, re-check:

```sh
claude-channel list
claude-channel status
claude-channel ask "From Codex: please reply by completing the channel request."
```

Only continue the fusion loop after a live target is listed and a test ask succeeds.

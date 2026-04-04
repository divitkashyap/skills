# Install GitHub MCP Server in OpenCode

## Prerequisites

1. OpenCode installed and configured
2. [GitHub Personal Access Token](https://github.com/settings/personal-access-tokens/new) with appropriate scopes
3. For local installation: [Docker](https://www.docker.com/) installed and running (optional)

## Remote Server Setup (Recommended)

The remote GitHub MCP Server is hosted by GitHub and provides the easiest method for getting started with OpenCode.

### Install steps

1. Open your OpenCode configuration file at `~/.config/opencode/opencode.json`
2. Add the GitHub MCP server configuration (see below)
3. Replace `YOUR_GITHUB_PAT` with your actual [GitHub Personal Access Token](https://github.com/settings/tokens)
4. Save the file
5. Restart OpenCode

### Streamable HTTP Configuration

```json
{
  "mcp": {
    "github": {
      "type": "remote",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_GITHUB_PAT"
      }
    }
  }
}
```

### With Environment Variable

To avoid hardcoding your token, use an environment variable:

```json
{
  "mcp": {
    "github": {
      "type": "remote",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${env:GITHUB_PAT}"
      }
    }
  }
}
```

Then export your PAT before running OpenCode:
```bash
export GITHUB_PAT=your_token_here
opencode
```

## Local Server Setup

The local GitHub MCP server can run via Docker or as a standalone binary.

### With Docker

1. Open your OpenCode configuration file at `~/.config/opencode/opencode.json`
2. Add the Docker-based configuration:
3. Replace `YOUR_GITHUB_PAT` with your actual [GitHub Personal Access Token](https://github.com/settings/tokens)
4. Save the file
5. Restart OpenCode

```json
{
  "mcp": {
    "github": {
      "type": "local",
      "command": ["docker", "run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_PAT"
      }
    }
  }
}
```

### With Environment Variable (Docker)

```json
{
  "mcp": {
    "github": {
      "type": "local",
      "command": ["docker", "run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_PAT}"
      }
    }
  }
}
```

### With Pre-built Binary (No Docker)

For environments without Docker, use the pre-built binary.

1. Download the [latest release binary](https://github.com/github/github-mcp-server/releases) for your platform
2. Make it executable and place it in your PATH:
```bash
chmod +x github-mcp-server
sudo mv github-mcp-server /usr/local/bin/
```
3. Add to your OpenCode configuration:

```json
{
  "mcp": {
    "github": {
      "type": "local",
      "command": ["github-mcp-server", "stdio"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_PAT"
      }
    }
  }
}
```

### Build from Source

If you have Go 1.24+ installed, build from source:

```bash
go build -o github-mcp-server ./cmd/github-mcp-server
```

Then use the binary path in your configuration:

```json
{
  "mcp": {
    "github": {
      "type": "local",
      "command": ["/path/to/github-mcp-server", "stdio"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_PAT"
      }
    }
  }
}
```

## Configuration File Location

- **Global**: `~/.config/opencode/opencode.json`
- **Project-specific**: `.opencode/opencode.json` in project root

OpenCode merges configurations, so you can set MCP servers globally and override per-project if needed.

## Security Best Practices

### Storing Your PAT Securely

1. **Use environment variables** instead of hardcoding your token
2. **Never commit** your token to version control
3. **Add to .gitignore** if using project-specific config:
```bash
echo ".opencode" >> .gitignore
```

### Token Scopes

For read-only access, grant only:
- `repo` (full repository access) or `repo:read` (read-only)
- `read:user` (user profile)
- `notifications` (if needed)

For full functionality including issue/PR management, `repo` scope is required.

## Verify Installation

1. Restart OpenCode completely
2. Run `/mcp` to list configured MCP servers
3. You should see `github` listed as an enabled server
4. Test with a query: "List my GitHub repositories"

## Troubleshooting

### Remote Server Issues

- **Connection errors**: Check your internet connection and firewall
- **Authentication failures**: Verify your PAT is valid and has correct scopes
- **Invalid token format**: Ensure no extra spaces in the Bearer token

### Local Server Issues

#### Docker Problems
- **Docker not running**: Start Docker Desktop or the Docker daemon
- **Image pull failures**: Try `docker logout ghcr.io` then restart
- **Permission denied**: Ensure your user has Docker permissions

#### Binary Problems
- **Command not found**: Verify the binary is in your PATH (`which github-mcp-server`)
- **Execution permissions**: Ensure the binary is executable (`chmod +x`)
- **Wrong architecture**: Download the correct binary for your OS (linux/amd64, linux/arm64, darwin/amd64, darwin/arm64, windows/amd64)

### General Issues

- **MCP not loading**: Check OpenCode logs for MCP-related errors
- **Invalid JSON**: Validate your opencode.json syntax
- **Server not responding**: Restart OpenCode after configuration changes
- **Tools not appearing**: Run `/mcp` to verify server is registered

### Using MCP Tools in OpenCode

Once configured, you can use GitHub MCP tools directly in your prompts:

```
Use the github tool to create a new issue in my repository
Use the github tool to list pull requests
Use the github tool to get file contents from my repo
```

## Important Notes

- **Docker image**: `ghcr.io/github/github-mcp-server` (official and supported)
- **npm package**: `@modelcontextprotocol/server-github` (deprecated as of April 2025 - no longer functional)
- **OpenCode specifics**: Uses `mcp` key for server configuration, supports both local and remote servers
- **Remote support**: OpenCode supports Streamable HTTP for remote MCP servers

## Additional Resources

- [OpenCode MCP Documentation](https://opencode.ai/docs/mcp-servers/)
- [GitHub MCP Server README](https://github.com/github/github-mcp-server)
- [GitHub Personal Access Token Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

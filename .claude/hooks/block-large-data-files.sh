#!/usr/bin/env bash
# Pre-tool-use hook: block commits/writes of large data files and known-secret patterns.
# Registered in .claude/settings.json under hooks.PreToolUse.

set -euo pipefail

input="$(cat)"
tool_name="$(echo "$input" | jq -r '.tool_name // empty')"
file_path="$(echo "$input" | jq -r '.tool_input.file_path // empty')"
command="$(echo "$input" | jq -r '.tool_input.command // empty')"

# Block writing files larger than 50MB or with sensitive extensions
if [[ -n "$file_path" ]]; then
  case "$file_path" in
    *.csv|*.parquet|*.feather|*.h5|*.hdf5)
      if [[ -f "$file_path" ]] && [[ "$(stat -c%s "$file_path" 2>/dev/null || echo 0)" -gt 52428800 ]]; then
        echo "BLOCKED: $file_path is >50MB. Large data files should not be committed. Add to .gitignore." >&2
        exit 2
      fi
      ;;
    *.env|*credentials*|*secret*|*api_key*)
      echo "BLOCKED: $file_path looks like a secret/credential file. Add to .gitignore and use CLAUDE.local.md for references." >&2
      exit 2
      ;;
  esac
fi

# Block git commits that include large data files or .env files
if [[ "$tool_name" == "Bash" ]] && [[ "$command" == *"git commit"* || "$command" == *"git add"* ]]; then
  if echo "$command" | grep -qE '\.(csv|parquet|feather|h5|hdf5)\b' ; then
    echo "WARNING: command appears to add data files. Confirm these belong in git, or add them to .gitignore." >&2
  fi
fi

exit 0

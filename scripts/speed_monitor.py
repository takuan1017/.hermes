#!/usr/bin/env python3
"""Speed monitor: measure provider latency and fallback if needed."""
import json, subprocess, sys, os, time, re

MODEL = "deepseek-chat"
PROVIDER = "deepseek"
THRESHOLD_S = 0.2
FALLBACK_MODEL = "claude-sonnet-4-5"
FALLBACK_PROVIDER = "anthropic"
CONFIG_PATH = os.path.expanduser("~/.hermes/config.yaml")

def measure_latency():
    """Measure time for a single chat completion via hermes CLI."""
    start = time.time()
    try:
        result = subprocess.run(
            ["hermes", "run", "-m", MODEL, "-p", "say 'ok' and nothing else"],
            capture_output=True, text=True, timeout=30
        )
        elapsed = time.time() - start
        return elapsed, result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return None, "", "timeout", -1
    except FileNotFoundError:
        return None, "", "hermes CLI not found", -1

def update_config(fallback_active: bool):
    """Update speed_monitor mode in config.yaml."""
    with open(CONFIG_PATH, 'r') as f:
        config = f.read()
    
    new_mode = "fallback" if fallback_active else "fast"
    
    if "speed_monitor:" in config:
        config = re.sub(
            r'(speed_monitor:\n\s+check_interval: \d+\n\s+fallback_model:.*?\n\s+fallback_provider:.*?\n\s+)mode: \w+',
            lambda m: m.group(1) + f"mode: {new_mode}",
            config
        )
    else:
        # No speed_monitor section, add it
        config += f"""
speed_monitor:
  check_interval: 300
  fallback_model: {FALLBACK_MODEL}
  fallback_provider: {FALLBACK_PROVIDER}
  mode: {new_mode}
  threshold_s: {THRESHOLD_S}
"""
    
    with open(CONFIG_PATH, 'w') as f:
        f.write(config)
    
    return new_mode

def main():
    # Check if we're already in fallback mode
    current_mode = "unknown"
    try:
        with open(CONFIG_PATH) as f:
            m = re.search(r'mode: (\w+)', f.read())
            if m:
                current_mode = m.group(1)
    except:
        pass
    
    latency, stdout, stderr, rc = measure_latency()
    
    if latency is None:
        print(f"SPEED_MONITOR|{MODEL}|FAILED|stderr={stderr.strip()}")
        if current_mode != "fallback":
            new_mode = update_config(True)
            print(f"SPEED_MONITOR|ACTION|Fell back to {FALLBACK_MODEL} ({FALLBACK_PROVIDER})")
        else:
            print(f"SPEED_MONITOR|INFO|Already in fallback mode, staying")
        return
    
    print(f"SPEED_MONITOR|{MODEL}|latency={latency:.3f}s|threshold={THRESHOLD_S}s|mode={current_mode}")
    
    needs_fallback = latency > THRESHOLD_S
    
    if needs_fallback and current_mode != "fallback":
        new_mode = update_config(True)
        print(f"SPEED_MONITOR|ACTION|Latency {latency:.3f}s exceeds {THRESHOLD_S}s threshold. "
              f"Fell back to {FALLBACK_MODEL} ({FALLBACK_PROVIDER})")
    elif not needs_fallback and current_mode == "fallback":
        new_mode = update_config(False)
        print(f"SPEED_MONITOR|ACTION|Latency {latency:.3f}s back under threshold. "
              f"Restored fast mode with {MODEL} ({PROVIDER})")
    else:
        print(f"SPEED_MONITOR|INFO|No change needed (latency={latency:.3f}s, mode={current_mode})")

if __name__ == "__main__":
    main()

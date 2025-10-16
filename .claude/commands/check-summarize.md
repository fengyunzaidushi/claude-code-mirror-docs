---
description: Check progress of parallel summarization or resume interrupted tasks
argument-hint: [action: status|resume|clean]
allowed-tools: Read, Write, Bash, Grep, Glob, SubAgent
model: sonnet
---

# Parallel Summarization Progress Monitor

Check and manage your parallel summarization tasks.

## Usage

### Check status

```bash
/check-summarize status
```

### Resume interrupted task

```bash
/check-summarize resume
```

### Clean up completed task files

```bash
/check-summarize clean
```

## Your Actions

### For `status`:

1. **Read progress files** in `progress/` directory:

   - Check for `task_layer*_batch*.json` files
   - Read task files to see which batches are defined
   - Check corresponding output files to see which are complete

2. **Report current state**:

   ```
   📊 PARALLEL SUMMARIZATION STATUS

   Layer 1: X/N completed (Y in progress, Z pending)
     ✅ Completed: batches 1, 2, 5
     ⏳ In progress: batches 3, 4, 6, 7
     ⏸️  Pending: batches 8, 9, 10

   Layer 2: Not started (waiting for Layer 1)

   Output directories:
     - section_summary01/: X files
     - section_summary02/: Y files
   ```

3. **Check for issues**:
   - Task files with no output after reasonable time (>10 min)
   - Suggest actions: retry, clean up, resume

### For `resume`:

1. **Identify incomplete batches**:

   - Find task files without corresponding output files
   - Determine which layer was in progress

2. **Relaunch failed/incomplete batches**:

   ```
   FOR each incomplete batch:
     Check if task file exists
     IF output file missing:
       Re-invoke: "Use batch-summarizer sub-agent to process task_layer{L}_batch{N}.json"
       Print: "🔄 Relaunched batch {N}"
     END IF
   END FOR
   ```

3. **Continue to next layer if current complete**:

   - If all batches in current layer done, check if next layer needed
   - If next layer needed, create task files and launch

4. **Report resume status**:

   ```
   🔄 RESUMING PARALLEL SUMMARIZATION

   Relaunched: 3 batches from Layer 1
   Status: Layer 1 - X/N completed

   Monitoring... (checking every 15 seconds)
   ```

### For `clean`:

1. **Clean up task files**:

   - Move or delete completed task files from `progress/`
   - Keep summary of what was completed
   - Preserve final output files

2. **Report cleanup**:

   ```
   🧹 CLEANUP COMPLETE

   Removed: 20 task files from progress/
   Preserved: Final summaries in section_summary01/, section_summary02/

   You can safely delete the progress/ directory if no longer needed.
   ```

## Task File Detection

Task files follow the pattern: `progress/task_layer{L}_batch{N}.json`

Each task file contains:

```json
{
  "layer": 1,
  "batch_id": 3,
  "output_file": "path/to/output.txt",
  ...
}
```

Check completion by verifying `output_file` exists.

## Edge Cases

**No task files found**:

```
ℹ️  No parallel summarization task found.
Use /parallel-summarize to start a new task.
```

**All complete**:

```
✅ All batches completed!
Final output: {final_summary_path}
Use /check-summarize clean to clean up task files.
```

**Some stuck**:

```
⚠️  Warning: 2 batches appear stuck (>10 min, no output)
  - Batch 5 (Layer 1): started {time} ago
  - Batch 8 (Layer 1): started {time} ago

Suggestions:
1. Use /check-summarize resume to retry
2. Check batch-summarizer logs for errors
3. Verify source files are accessible
```

## Integration with /parallel-summarize

This command complements `/parallel-summarize`:

- `/parallel-summarize`: Start new parallel summarization
- `/check-summarize status`: Monitor progress
- `/check-summarize resume`: Resume if interrupted
- `/check-summarize clean`: Clean up when done

## Example Workflow

```bash
# Start the task
/parallel-summarize D:/novels/chapters/ 30 D:/novels/summaries/

# (User goes away, comes back later)

# Check what happened
/check-summarize status

# Resume if needed
/check-summarize resume

# Clean up when done
/check-summarize clean
```

Remember: You're managing the orchestration. The actual summarization work is done by batch-summarizer sub-agents. Your job is to track, monitor, and coordinate.

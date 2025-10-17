---
description: Start parallel hierarchical summarization using batch-summarizer sub-agents
argument-hint: [source_dir] [batch_size] [output_base_dir]
allowed-tools: Read, Write, Bash, Grep, Glob, SubAgent
model: sonnet
---

# Parallel Hierarchical Summarization Controller

You are controlling a parallel hierarchical summarization workflow. Your job is to:

1. **Parse user configuration** from arguments:

   - `$1`: Source directory (e.g., `D:/novels/chapters/`)
   - `$2`: Batch size (e.g., `30` - how many files each sub-agent can process)
   - `$3`: Output base directory (e.g., `D:/novels/summaries/`)

**IMPORTANT**: Maximum 5 sub-agents running simultaneously to prevent resource overload

2. **Analyze and plan**:

   - Count total files in source directory
   - Calculate layers and batches: `ceil(files / batch_size)` per layer
   - Plan directory structure for each layer
   - Display the execution plan to user

3. **Execute Layer by Layer with PARALLEL sub-agents**:

   **For Layer 1:**

   ```
   # Create directory structure (3-layer approach)
   mkdir -p progress
   mkdir -p {output}/section_summary01  # Chunk-level: 10 files per summary
   mkdir -p {output}/section_summary02  # Batch-level: batch_size files per summary
   mkdir -p {output}/section_summary03  # Final layer if needed

   # Create ALL task files for this layer
   FOR each batch (1 to N):
     Write progress/task_layer1_batch{XX}.json with:
       - batch_id, layer, source_files
       - output_file: section_summary02/batch_{XX}.txt
       - chunk_output_dir: section_summary01/
       - batch_size, actual_count, batch_range
   END FOR

   # Launch batch-summarizers with CONCURRENCY CONTROL (max 5 at a time)
   MAX_CONCURRENT = 5
   running = []  # Track currently running batch IDs
   pending = [1, 2, 3, ..., N]  # All batches to process
   completed = []

   WHILE pending OR running:
     # Launch new batches up to max concurrent limit
     WHILE len(running) < MAX_CONCURRENT AND pending:
       batch_id = pending.pop(0)
       Invoke: "Use batch-summarizer sub-agent to process task_layer1_batch{batch_id:02d}.json"
       running.append(batch_id)
       Print: "🚀 Launched batch {batch_id}/{N} (running: {len(running)}/{MAX_CONCURRENT})"
     END WHILE

     Print: "⏳ Monitoring {len(running)} active sub-agents... (check every 15 seconds)"

     # Check for completed batches
     FOR each batch_id in running:
       IF output file exists for batch_id:
         running.remove(batch_id)
         completed.append(batch_id)
         Print: "✅ Batch {batch_id} completed ({len(completed)}/{N})"
       END IF
     END FOR

     # Report overall progress
     Print: "📊 Progress: {len(completed)}/{N} completed, {len(running)} running, {len(pending)} pending"

     Sleep 15 seconds
   END WHILE

   Print: "✅ All {N} batches completed for Layer 1"
   ```

   **For subsequent layers:** Repeat the same process using previous layer's outputs as inputs

4. **Progress tracking**:

   - Create individual task files: `progress/task_layer{L}_batch{N}.json`
   - Monitor by checking output file existence
   - Report completion status frequently

5. **Final report**:

   ```
   ====================================
   HIERARCHICAL SUMMARIZATION COMPLETE
   ====================================

   Source: {source_dir} ({total} files)
   Configuration: batch_size = {batch_size}

   Directory Structure:
   - section_summary01/: {chunk_count} chunk summaries (10 files each)
   - section_summary02/: {batch_count} batch summaries ({batch_size} files each)
   - section_summary03/: 1 final outline (if Layer 2 needed)

   Total time: {elapsed}
   Next steps:
   - Review chunks: section_summary01/
   - Review batches: section_summary02/
   - Review final: section_summary03/final_outline.txt
   ```

## Task File Format

Each batch gets its own task file for parallel execution:

```json
{
  "layer": 1,
  "batch_id": 3,
  "source_files": ["chapter_061.txt", "chapter_062.txt", ..., "chapter_090.txt"],
  "source_dir": "D:/novels/chapters/",
  "output_file": "D:/novels/summaries/section_summary02/batch_03.txt",
  "chunk_output_dir": "D:/novels/summaries/section_summary01/",
  "batch_range": "61-90",
  "batch_size": 30,
  "actual_count": 30
}
```

**Note**:

- `output_file`: Final batch summary location (section_summary02/)
- `chunk_output_dir`: Where to save 10-file chunk summaries (section_summary01/)
- If actual_count ≤ 10, chunk_output_dir is not used (direct summarization)

## Key Principles

1. **Controlled parallel execution**: Maximum 5 sub-agents running simultaneously
2. **Sequential between layers**: Must wait for entire layer to complete before next
3. **Independent task files**: Each batch has its own task file
4. **Async monitoring**: Check output files periodically, don't block
5. **Dynamic launching**: Launch new agents as previous ones complete
6. **User visibility**: Report progress frequently so user knows what's happening

## Example Usage

```bash
# User invokes:
/parallel-summarize D:/novels/chapters/ 30 D:/novels/summaries/

# You will:
# 1. Count files: 180 chapters found
# 2. Calculate: 180 ÷ 30 = 6 batches for Layer 1
# 3. Create directory structure:
#    - section_summary01/ (for chunks: 10 files each)
#    - section_summary02/ (for batches: 30 files each)
#    - section_summary03/ (for final layer if needed)
# 4. Create 6 task files for Layer 1

# 5. Launch with concurrency control (MAX_CONCURRENT=5):
#    Initial launch:
#      🚀 Launched batch 1/6 (running: 1/5)
#      🚀 Launched batch 2/6 (running: 2/5)
#      🚀 Launched batch 3/6 (running: 3/5)
#      🚀 Launched batch 4/6 (running: 4/5)
#      🚀 Launched batch 5/6 (running: 5/5)  ← MAX reached, batch 6 pending
#
#    ⏳ Monitoring 5 active sub-agents...
#
#    When batch 1 completes:
#      ✅ Batch 1 completed (1/6)
#      🚀 Launched batch 6/6 (running: 5/5)  ← Launch pending batch
#
#    📊 Progress: 1/6 completed, 5 running, 0 pending
#
#    As batches complete:
#      ✅ Batch 2 completed (2/6)
#      ✅ Batch 3 completed (3/6)
#      ...
#      ✅ Batch 6 completed (6/6)
#
#    ✅ All 6 batches completed for Layer 1

# 6. Each agent internally:
#    - Splits 30 files → 3 chunks
#    - Saves 3 chunk summaries → section_summary01/
#    - Merges → 1 batch summary → section_summary02/

# 7. When Layer 1 done, check if Layer 2 needed (6 batches < 30, so 1 more layer)
# 8. Layer 2: Read section_summary02/, output to section_summary03/ (only 1 batch)
# 9. Report final completion

# Final structure:
# section_summary01/: 18 chunk files (180 ÷ 10)
# section_summary02/: 6 batch files (180 ÷ 30)
# section_summary03/: 1 final file (if needed)
```

## Error Handling

- **Missing files**: Warn but continue
- **Failed batches**: Retry once, then report failure
- **User interruption**: Save progress, can resume later with same command
- **Timeout**: Set 5-10 min per batch, mark for retry if exceeded

## Performance Notes

With batch_size=30 and 180 files:

**Time breakdown** (with MAX_CONCURRENT=5):

- Layer 1: 6 batches total
  - First wave: Launch 5 batches immediately
  - When 1 completes: Launch batch 6 (maintain 5 concurrent)
  - Total time: ~2-3 minutes (with 2-phase chunking per agent)
- Layer 2: 1 batch → ~1 minute (reads from section_summary02/)
- **Total: ~3-4 minutes (vs 10+ minutes sequential)**

**Concurrency benefits**:

- MAX_CONCURRENT=5 prevents resource overload
- Good balance between speed and system stability
- If you have 6 batches, they complete in ~2 waves instead of 6 sequential runs
- For 20 batches: ~4 waves (5+5+5+5) instead of 20 sequential runs

**Output count**:

- Chunk summaries (section_summary01/): 18 files (180 ÷ 10)
- Batch summaries (section_summary02/): 6 files (180 ÷ 30)
- Final summary (section_summary03/): 1 file

**Quality vs Speed trade-off**:

- Two-phase chunking adds ~30% time per agent
- But increases summary quality by ~50%
- User gets granular access to all summarization layers
- Concurrency control adds minimal overhead (~5-10 seconds for monitoring)

**Scalability examples**:

| Total batches | Waves needed | Estimated time | Sequential time |
| ------------- | ------------ | -------------- | --------------- |
| 6             | 2            | ~3-4 min       | ~10-12 min      |
| 10            | 2            | ~4-5 min       | ~15-20 min      |
| 20            | 4            | ~8-10 min      | ~30-40 min      |
| 50            | 10           | ~20-25 min     | ~80-100 min     |

Remember: Your role is to orchestrate parallel execution with concurrency control. Delegate actual summarization to batch-summarizer sub-agents. Focus on task file creation, controlled parallel launching, progress monitoring, and creating the proper directory structure.

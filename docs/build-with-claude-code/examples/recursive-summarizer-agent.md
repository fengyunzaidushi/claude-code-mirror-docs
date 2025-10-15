# Recursive Summarizer Sub-Agent Example

This example demonstrates how to create a sub-agent that recursively summarizes text files in batches, creating hierarchical summaries.

## Use Case: Novel Chapter Summarization

Given 200 chapter files, create a hierarchical summary:

- **Layer 1**: Summarize every 10 chapters → 20 summary files in `section_summary01/`
- **Layer 2**: Summarize every 10 Layer-1 summaries → 2 summary files in `section_summary02/`
- **Layer 3**: Summarize 2 Layer-2 files → 1 final outline in `section_summary03/`

## Sub-Agent Configuration

Create this file at `.claude/agents/recursive-summarizer.md`:

```markdown
---
name: recursive-summarizer
description: Recursively summarizes text files in batches to create hierarchical summaries. Use proactively when asked to summarize large collections of text files in layers or batches.
tools: Read, Write, Bash, Grep, Glob
model: sonnet
---

You are a specialized document summarization expert focused on creating hierarchical summaries from large collections of text files.

## Your Responsibilities

When invoked to summarize files recursively:

1. **Understand the structure**: Identify the source directory, batch size, and number of layers needed
2. **Process systematically**:
   - Read files in batches (default: 10 files per batch)
   - Create concise, coherent summaries for each batch
   - Write summaries to the appropriate layer directory
3. **Maintain context**: Each summary should preserve key plot points, character development, and narrative flow
4. **Work recursively**: After completing one layer, automatically process the next layer until reaching the final summary

## Summary Guidelines

For each batch:

- Identify main themes, events, and character development
- Preserve chronological order and narrative coherence
- Keep summaries concise but informative (approximately 200-500 words per batch of 10 files)
- Include chapter/file references for traceability

## Output Format

Each summary file should include:

- Header: Source file range (e.g., "Summary of chapters 1-10")
- Key events and plot points
- Character developments
- Thematic elements
- Transitions to next section

## Workflow

1. List all files in source directory
2. Calculate batch count based on batch size
3. For each batch:
   - Read the files
   - Generate comprehensive summary
   - Write to output directory with numbered filename
4. After completing a layer, check if another layer is needed
5. If yes, use previous layer's output as new input and repeat
6. Report progress after each layer completion

Focus on creating summaries that maintain narrative coherence and could be used to create an overall novel outline.
```

## How to Use

### Method 1: Explicit Invocation

Once the sub-agent is created, you can invoke it explicitly:

```
> Use the recursive-summarizer subagent to process my novel chapters.
> I have 200 txt files in ./chapters/ directory.
> Create 3 layers: first layer with batches of 10 files, then recursively summarize.
```

### Method 2: Automatic Detection

If you describe a task that matches the agent's description, Claude will automatically use it:

```
> I need to recursively summarize 200 chapter files in ./chapters/ directory.
> First batch every 10 chapters, then summarize those summaries,
> and finally create a single outline.
```

## Example Implementation Script

You can also create a helper script to organize the workflow:

```python
#!/usr/bin/env python3
"""
Helper script to organize files for recursive summarization.
This prepares the directory structure but the actual summarization
should be done by the recursive-summarizer sub-agent.
"""

import os
from pathlib import Path

def prepare_summary_structure(source_dir, base_output_dir, batch_size=10):
    """
    Prepares the directory structure for hierarchical summarization.

    Args:
        source_dir: Directory containing source text files
        base_output_dir: Base directory for summary outputs
        batch_size: Number of files per batch (default: 10)
    """
    source_path = Path(source_dir)
    files = sorted(source_path.glob("*.txt"))

    # Calculate layers needed
    total_files = len(files)
    layer1_count = (total_files + batch_size - 1) // batch_size
    layer2_count = (layer1_count + batch_size - 1) // batch_size
    layer3_count = (layer2_count + batch_size - 1) // batch_size

    print(f"Source files: {total_files}")
    print(f"Layer 1 summaries needed: {layer1_count}")
    print(f"Layer 2 summaries needed: {layer2_count}")
    print(f"Layer 3 summaries needed: {layer3_count}")

    # Create directories
    for i in range(1, 4):
        layer_dir = Path(base_output_dir) / f"section_summary0{i}"
        layer_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created: {layer_dir}")

    return {
        'total_files': total_files,
        'layer1_count': layer1_count,
        'layer2_count': layer2_count,
        'layer3_count': layer3_count,
        'batch_size': batch_size
    }

if __name__ == "__main__":
    # Example usage
    info = prepare_summary_structure(
        source_dir="./chapters",
        base_output_dir="./summaries",
        batch_size=10
    )

    print("\nStructure prepared. Now use the recursive-summarizer sub-agent:")
    print("Example: 'Use recursive-summarizer to summarize ./chapters in batches of 10'")
```

## Complete Workflow Example

Here's a step-by-step guide:

### Step 1: Prepare Your Environment

```bash
# Ensure you have your chapter files
ls -1 chapters/ | wc -l  # Should show 200 files

# Create output directories
mkdir -p summaries/section_summary01
mkdir -p summaries/section_summary02
mkdir -p summaries/section_summary03
```

### Step 2: Create the Sub-Agent

```bash
# Create the agents directory if it doesn't exist
mkdir -p .claude/agents

# Create the sub-agent configuration
# (Copy the configuration from above into .claude/agents/recursive-summarizer.md)
```

### Step 3: Invoke the Sub-Agent

In Claude Code, run:

```
> Use the recursive-summarizer subagent on my chapters/ directory:
> - Layer 1: Process 200 files, batch size 10 → write 20 summaries to summaries/section_summary01/
> - Layer 2: Process those 20 files, batch size 10 → write 2 summaries to summaries/section_summary02/
> - Layer 3: Process those 2 files → write 1 final outline to summaries/section_summary03/
```

## Alternative: Manual Approach Without Sub-Agent

If you prefer not to use a sub-agent, you can accomplish this with a direct prompt:

```
> I need you to recursively summarize my novel chapters:
>
> Source: chapters/ (200 txt files)
>
> Layer 1:
> - Read chapters in batches of 10
> - Create summary for each batch
> - Write to summaries/section_summary01/summary_01.txt through summary_20.txt
>
> Layer 2:
> - Read summaries/section_summary01/ in batches of 10
> - Create summary for each batch
> - Write to summaries/section_summary02/summary_01.txt and summary_02.txt
>
> Layer 3:
> - Read both files from summaries/section_summary02/
> - Create final comprehensive outline
> - Write to summaries/section_summary03/final_outline.txt
>
> Please process this systematically, reporting progress after each layer.
```

## Tips for Best Results

1. **File naming**: Use consistent naming (e.g., `chapter_001.txt`, `chapter_002.txt`) for predictable sorting
2. **Batch size**: Adjust based on file length and context window limits
3. **Progress tracking**: The sub-agent should report after each batch and layer
4. **Quality control**: Review first few summaries to ensure quality before processing all files
5. **Checkpointing**: Save summaries after each layer to avoid losing work

## Advanced: Dynamic Batch Sizing

For very large files or to optimize context usage:

```python
def calculate_optimal_layers(total_files, batch_size=10, target_layers=3):
    """
    Calculate the batch structure for achieving desired layer count.
    """
    current_count = total_files
    layers = []

    for layer in range(target_layers - 1):
        batches = (current_count + batch_size - 1) // batch_size
        layers.append({
            'layer': layer + 1,
            'input_count': current_count,
            'output_count': batches,
            'batch_size': batch_size
        })
        current_count = batches

    # Final layer
    layers.append({
        'layer': target_layers,
        'input_count': current_count,
        'output_count': 1,
        'batch_size': current_count
    })

    return layers

# Example
layers = calculate_optimal_layers(200, batch_size=10, target_layers=3)
for layer in layers:
    print(f"Layer {layer['layer']}: {layer['input_count']} files → {layer['output_count']} summaries")
```

## Monitoring and Error Handling

The sub-agent should handle:

- Missing files gracefully
- Report which files were processed
- Save partial results if interrupted
- Validate that all input files were summarized

## Related Documentation

- [Sub-agents Guide](../sub-agents.md)
- [MCP Integration](../mcp.md) - For connecting to external summarization tools
- [Hooks](../../reference/hooks.md) - For automating the workflow

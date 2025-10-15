#!/usr/bin/env python3
"""
Preparation script for recursive hierarchical summarization.

This script prepares the directory structure and calculates the layering
needed for hierarchical summarization of large document collections.

The actual summarization should be performed by the recursive-summarizer sub-agent.

Example usage:
    python prepare-recursive-summary.py --source ./chapters --output ./summaries --batch-size 10
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple
import sys


def count_files(directory: Path, pattern: str = "*.txt") -> int:
    """Count files matching pattern in directory."""
    return len(list(directory.glob(pattern)))


def calculate_layer_structure(total_files: int, batch_size: int = 10) -> List[Dict]:
    """
    Calculate the hierarchical structure needed for summarization.
    
    Args:
        total_files: Number of source files
        batch_size: Number of files to summarize per batch
    
    Returns:
        List of dictionaries describing each layer
    """
    layers = []
    current_count = total_files
    layer_num = 1
    
    while current_count > 1:
        batches_needed = (current_count + batch_size - 1) // batch_size
        
        layers.append({
            'layer': layer_num,
            'input_count': current_count,
            'output_count': batches_needed,
            'batch_size': min(batch_size, current_count),
            'source_dir': f'section_summary{layer_num-1:02d}' if layer_num > 1 else 'source',
            'output_dir': f'section_summary{layer_num:02d}'
        })
        
        current_count = batches_needed
        layer_num += 1
    
    return layers


def create_directory_structure(base_output_dir: Path, layers: List[Dict]) -> None:
    """Create the directory structure for all summary layers."""
    for layer in layers:
        layer_dir = base_output_dir / layer['output_dir']
        layer_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {layer_dir}")


def generate_summary_manifest(
    source_dir: Path,
    output_dir: Path,
    layers: List[Dict],
    file_pattern: str
) -> Dict:
    """
    Generate a manifest file with all the information needed for summarization.
    
    This manifest can be read by the sub-agent to understand the task.
    """
    source_files = sorted(source_dir.glob(file_pattern))
    
    manifest = {
        'source_directory': str(source_dir.absolute()),
        'output_directory': str(output_dir.absolute()),
        'file_pattern': file_pattern,
        'total_source_files': len(source_files),
        'source_files': [f.name for f in source_files],
        'layers': layers,
        'instructions': {
            'description': 'Hierarchical summarization task',
            'process': 'Process each layer sequentially, using output from previous layer as input for next',
            'batch_processing': 'Read and summarize files in batches according to batch_size',
            'output_naming': 'Name files as summary_01.txt, summary_02.txt, etc.',
            'final_output': f"Final summary will be in {layers[-1]['output_dir']}"
        }
    }
    
    return manifest


def save_manifest(manifest: Dict, output_dir: Path) -> Path:
    """Save the manifest to a JSON file."""
    manifest_path = output_dir / 'summary_manifest.json'
    with manifest_path.open('w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return manifest_path


def print_summary_plan(layers: List[Dict], total_files: int) -> None:
    """Print a human-readable summary of the layering plan."""
    print("\n" + "="*70)
    print("HIERARCHICAL SUMMARIZATION PLAN")
    print("="*70)
    print(f"\nTotal source files: {total_files}")
    print(f"Total layers needed: {len(layers)}")
    print(f"\nLayer breakdown:\n")
    
    for layer in layers:
        print(f"Layer {layer['layer']}:")
        print(f"  Input:  {layer['input_count']} files from {layer['source_dir']}")
        print(f"  Output: {layer['output_count']} summaries to {layer['output_dir']}")
        print(f"  Batch:  {layer['batch_size']} files per summary")
        print()
    
    print("="*70)


def generate_claude_prompt(manifest: Dict) -> str:
    """Generate a prompt for Claude Code to execute the summarization."""
    layers = manifest['layers']
    
    prompt = f"""Use the recursive-summarizer subagent to process my documents:

Source: {manifest['source_directory']} ({manifest['total_source_files']} files)
Output: {manifest['output_directory']}

"""
    
    for layer in layers:
        prompt += f"""Layer {layer['layer']}:
- Read {layer['input_count']} files from {layer['source_dir']}
- Create {layer['output_count']} summaries (batch size: {layer['batch_size']})
- Write to {layer['output_dir']}/summary_XX.txt

"""
    
    prompt += """Please process systematically, reporting progress after each batch and layer.
Save the final comprehensive summary/outline in the last layer directory.
"""
    
    return prompt


def main():
    parser = argparse.ArgumentParser(
        description='Prepare directory structure for recursive hierarchical summarization'
    )
    parser.add_argument(
        '--source',
        type=str,
        required=True,
        help='Source directory containing files to summarize'
    )
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output directory for summary layers'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Number of files to summarize per batch (default: 10)'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        default='*.txt',
        help='File pattern to match (default: *.txt)'
    )
    parser.add_argument(
        '--generate-prompt',
        action='store_true',
        help='Generate a Claude Code prompt for the summarization task'
    )
    
    args = parser.parse_args()
    
    # Validate source directory
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"Error: Source directory '{source_dir}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Count source files
    total_files = count_files(source_dir, args.pattern)
    if total_files == 0:
        print(f"Error: No files matching '{args.pattern}' found in '{source_dir}'", file=sys.stderr)
        sys.exit(1)
    
    print(f"\nFound {total_files} files in {source_dir}")
    
    # Calculate layer structure
    layers = calculate_layer_structure(total_files, args.batch_size)
    
    # Print the plan
    print_summary_plan(layers, total_files)
    
    # Create output directory structure
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nCreating directory structure in {output_dir}...\n")
    create_directory_structure(output_dir, layers)
    
    # Generate and save manifest
    manifest = generate_summary_manifest(source_dir, output_dir, layers, args.pattern)
    manifest_path = save_manifest(manifest, output_dir)
    print(f"\n✓ Saved manifest to: {manifest_path}")
    
    # Generate Claude prompt if requested
    if args.generate_prompt:
        prompt = generate_claude_prompt(manifest)
        prompt_path = output_dir / 'claude_prompt.txt'
        with prompt_path.open('w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"✓ Saved Claude prompt to: {prompt_path}")
        print("\n" + "="*70)
        print("COPY THIS PROMPT TO CLAUDE CODE:")
        print("="*70)
        print(prompt)
        print("="*70)
    
    print("\n✅ Preparation complete!")
    print("\nNext steps:")
    print("1. Review the layer structure above")
    print("2. In Claude Code, use the recursive-summarizer subagent with the generated prompt")
    print(f"3. Or manually run: cat {output_dir}/claude_prompt.txt")
    print("\nAlternatively, invoke directly in Claude Code:")
    print(f"  'Process {source_dir} using recursive-summarizer with batch size {args.batch_size}'")


if __name__ == '__main__':
    main()


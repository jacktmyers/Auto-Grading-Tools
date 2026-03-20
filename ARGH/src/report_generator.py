import os
from datetime import datetime


def generate_report(student_name, files, config):
    report_lines = []
    report_lines.append(f"# {student_name} | Lab {config['assignment_number']} | AI Report\n")

    if not files:
        report_lines.append("No files analyzed.\n")
        return

    files.sort(key=lambda x: (x.get('commit_date', 0), x.get('assignment_related_score', 0)), reverse=True)

    report_lines.append("## Metric Averages")
    for metric in config["metrics"]:
        scores = [f[metric + '_score'] for f in files if f.get(metric + '_score') is not None]
        avg = sum(scores) / len(scores) if scores else 0
        report_lines.append(f"* **{metric.replace('_', ' ').title()}**: {avg:.2f}\n")
    
    report_lines.append("\n## Individual Files\n")

    headers = ["File", "Keyword Count", "Emoji Count", "Last Commit Date", "Last Commit Message"]
    for metric in config["metrics"]:
        headers.append(f"{metric.replace('_', ' ').title()} Score")
    headers.append("Assignment Related Score")

    report_lines.append("| " + " | ".join(headers) + " |")
    report_lines.append("|" + "|".join(["--------" for _ in headers]) + "|")

    for file_entry in files:
        relative_path = os.path.relpath(file_entry['path'], os.path.join(config["assignment_directory"], student_name.replace(" ","-")))
        
        row = []
        row.append(relative_path)
        row.append(str(file_entry['keyword_count']))
        row.append(str(file_entry['emoji_count']))

        if file_entry.get('commit_date'):
            commit_date = datetime.fromtimestamp(file_entry['commit_date']).strftime("%m/%d/%y")
            row.append(commit_date)
        else:
            row.append("")

        if file_entry.get('commit_msg'):
            row.append(file_entry['commit_msg'])
        else:
            row.append("")

        for metric in config["metrics"]:
            score_key = f"{metric}_score"
            if file_entry.get(score_key) is not None:
                row.append(str(file_entry[score_key]))
            else:
                row.append("")

        if file_entry.get("assignment_related_score") is not None:
            row.append(str(file_entry['assignment_related_score']))
        else:
            row.append("")

        report_lines.append("| " + " | ".join(row) + " |")

    report_lines.append("\n## Emoji Lines\n")
    for file_entry in files:
        if file_entry.get('emoji_locations'):
            relative_path = os.path.relpath(file_entry['path'], os.path.join(config["assignment_directory"], student_name.replace(" ","-")))
            emoji_lines = []
            for e in file_entry.get('emoji_locations'):
                emoji_lines.append(f"{e['line_num']+1}: {e['line']}")
            joined_lines="\n".join(emoji_lines)
            report_lines.append(f"### {relative_path}\n\n```\n{joined_lines}\n```\n")

    report_lines.append("\n## AI Models Used\n")
    report_lines.append(f"* **Keyword Generation**: {config['keyword']}")
    report_lines.append(f"* **Metrics**: {config['metric']}")
    report_lines.append(f"* **Assignment Relation**: {config['matcher']}")


    report_content = "\n".join(report_lines)

    report_path = os.path.join(config["assignment_directory"], student_name.replace(" ","-"), config["report_location"])
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

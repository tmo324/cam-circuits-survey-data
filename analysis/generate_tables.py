"""Generate the six paper tables as reusable LaTeX fragments."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from common import ROOT


DATA_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "tables" / "generated"


def read_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / filename, keep_default_na=False)


def escape_latex(value: object) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text


def write_table(filename: str, lines: list[str]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / filename
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")
    return output


def generate_table_01() -> None:
    data = read_csv("table01_cam_concepts.csv")
    lines = [
        r"\begin{table}[b]",
        r"\caption{Types of CAM concepts.}",
        r"\label{tab_cam_concepts}",
        r"\centering",
        r"\begin{tabular}{|l|l|l|l|}",
        r"\hline",
        r"\textbf{Input} & \textbf{Storage (B or T)} & \textbf{Output} & \textbf{Circuit} \\ \hline",
    ]
    for row in data.itertuples(index=False):
        circuit = f"{escape_latex(row.circuit)} \\cite{{{row.citation_key}}}"
        lines.append(
            f"{row.input} & {row.storage} & {row.output} & {circuit} \\\\ \\hline"
        )
    lines.extend([r"\end{tabular}", r"\end{table}"])
    write_table("table01_cam_concepts.tex", lines)


def generate_table_02() -> None:
    lines = [
        r"\begin{table}[t]",
        r"\caption{Cell designs for binary and ternary CAM using SRAM (10T binary, 16T ternary) and DRAM (3T1C binary, 6T2C ternary) technologies \cite{SRAM_5,DRAM_20,DRAM_22}.}",
        r"\label{tab:circuit_examples_SC}",
        r"\centering",
        r"\begin{tabular}{|c|c|c|}",
        r"\hline",
        r" & \textbf{SRAM} & \textbf{DRAM} \\ \hline",
        r"\rotatebox{90}{\textbf{Binary}} &",
        r"\includegraphics[height=2.3cm]{tables/assets/table02_sram_binary.png} &",
        r"\includegraphics[height=2.3cm]{tables/assets/table02_dram_binary.png} \\ \hline",
        r"\rotatebox{90}{\textbf{Ternary}} &",
        r"\includegraphics[height=2.3cm]{tables/assets/table02_sram_ternary.png} &",
        r"\includegraphics[height=2.3cm]{tables/assets/table02_dram_ternary.png} \\ \hline",
        r"\end{tabular}",
        r"\end{table}",
    ]
    write_table("table02_sram_dram_cell_schematics.tex", lines)


def generate_table_03() -> None:
    lines = [
        r"\begin{table}[t]",
        r"\caption{Cell designs for CAM using emerging non-volatile technologies: Ternary ReRAM (2T2M) \cite{ReRAM_7}, Ternary MTJ (4T2MTJ) \cite{MTJ_2}, Ternary FeFET (4T2FeFET) \cite{FeFET_1}, Analog ReRAM (6T2M) \cite{ReRAM_5}, and differentiable ReRAM (6T2M) \cite{types_dcam}.}",
        r"\label{tab:circuit_examples_NVM}",
        r"\centering",
        r"\begin{tabular}{|c|c|c|c|}",
        r"\hline",
        r" & \textbf{ReRAM} & \textbf{MTJ} & \textbf{FeFET} \\ \hline",
        r"\rotatebox{90}{\textbf{Ternary}} &",
        r"\includegraphics[height=2.0cm]{tables/assets/table03_reram_ternary.png} &",
        r"\includegraphics[height=2.0cm]{tables/assets/table03_mtj_ternary.png} &",
        r"\includegraphics[height=2.0cm]{tables/assets/table03_fefet_ternary.png} \\ \hline",
        r"\rotatebox{90}{\textbf{Analog}} &",
        r"\includegraphics[height=2.1cm]{tables/assets/table03_reram_analog.png} &",
        r" &",
        r"\includegraphics[height=2.1cm]{tables/assets/table03_fefet_analog.png} \\ \hline",
        r"\rotatebox{90}{\textbf{Differentiable}} &",
        r"\includegraphics[height=2.1cm]{tables/assets/table03_reram_differentiable.png} &",
        r" & \\ \hline",
        r"\end{tabular}",
        r"\end{table}",
    ]
    write_table("table03_nvm_cell_schematics.tex", lines)


def generate_table_04() -> None:
    data = read_csv("table04_cam_technology_comparison.csv")
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Comparison of CAM Technologies}",
        r"\label{tab:cam_comparison}",
        r"\begin{tabular}{|l|l|l|l|}",
        r"\hline",
        r"\textbf{Feature} & \textbf{SRAM CAM} & \textbf{DRAM CAM} & \textbf{NVM CAM} \\ \hline",
    ]
    for row in data.itertuples(index=False):
        values = [escape_latex(value) for value in row]
        lines.append(" & ".join(values) + r" \\ \hline")
    lines.extend([r"\end{tabular}", r"\end{table}"])
    write_table("table04_cam_technology_comparison.tex", lines)


def format_float(value: object) -> str:
    if value == "":
        return "--"
    return f"{float(value):.2f}"


def generate_table_05() -> None:
    data = read_csv("table05_cam_cell_designs.csv")
    lines = [
        r"\begin{table*}[t]",
        r"\small",
        r"\caption{CAM Cell Designs.}",
        r"\label{tab:cam_cell_designs}",
        r"\centering",
        r"\begin{tabular}{cccccc}",
        r"\hline",
        r"Design & Technology & Process Node (nm) & Area ($\mu\mathrm{m}^2$) & Search Energy (fJ/bit/search) & Year \\ \hline",
    ]
    for row in data.itertuples(index=False):
        design = escape_latex(row.design)
        energy = format_float(row.search_energy_fj_per_bit_per_search)
        lines.append(
            f"{design}~\\cite{{{row.citation_key}}} & "
            f"{row.technology} & {int(row.process_node_nm)} & "
            f"{float(row.area_um2):.2f} & {energy} & {int(row.year)} \\\\"
        )
    lines.extend([r"\hline", r"\end{tabular}", r"\end{table*}"])
    write_table("table05_cam_cell_designs.tex", lines)


def generate_table_06() -> None:
    data = read_csv("cam_applications.csv")
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Performance Improvements Over SOTA Across CAM-Based Applications}",
        r"\label{tab:fom}",
        r"\begin{tabular}{|l|p{3.3cm}|p{4.3cm}|}",
        r"\hline",
        r"\textbf{Year} & \textbf{Application} & \textbf{Improvement} \\ \hline",
    ]
    for row in data.itertuples(index=False):
        application = escape_latex(row.application)
        improvement = escape_latex(row.improvement)
        lines.append(
            f"{int(row.year)} & {application} \\cite{{{row.citation_key}}} & "
            f"{improvement} \\\\ \\hline"
        )
    lines.extend([r"\end{tabular}", r"\end{table}"])
    write_table("table06_application_improvements.tex", lines)


def main() -> None:
    generate_table_01()
    generate_table_02()
    generate_table_03()
    generate_table_04()
    generate_table_05()
    generate_table_06()


if __name__ == "__main__":
    main()

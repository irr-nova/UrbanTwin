import sys
from pathlib import Path

import pandas as pd

AI_DIRECTORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AI_DIRECTORY))

from preprocessing.parse_sumo import parse_edge_data


def test_parser_reads_edge_data_and_converts_numeric_values(tmp_path):
    xml_file = tmp_path / "edge_data.xml"
    xml_file.write_text(
        """
        <meandata>
            <interval begin="0" end="3600">
                <edge id="edge_1"
                      sampledSeconds="100"
                      flow="25.5"
                      speed="12.5"
                      traveltime="8"
                      waitingTime="2"
                      timeLoss="3"
                      density="4"
                      occupancy="5"/>
            </interval>
        </meandata>
        """,
        encoding="utf-8",
    )

    df = parse_edge_data(xml_file)

    assert len(df) == 1
    assert df.iloc[0]["edge_id"] == "edge_1"
    assert df.iloc[0]["interval_begin"] == 0
    assert df.iloc[0]["interval_end"] == 3600
    assert df.iloc[0]["sampled_seconds"] == 100
    assert df.iloc[0]["flow"] == 25.5
    assert df.iloc[0]["speed"] == 12.5


def test_parser_excludes_edges_without_positive_sampled_seconds(tmp_path):
    xml_file = tmp_path / "edge_data.xml"
    xml_file.write_text(
        """
        <meandata>
            <interval begin="0" end="3600">
                <edge id="observed" sampledSeconds="100" speed="10"/>
                <edge id="unobserved" sampledSeconds="0" speed="0"/>
                <edge id="missing" speed="10"/>
            </interval>
        </meandata>
        """,
        encoding="utf-8",
    )

    df = parse_edge_data(xml_file)

    assert df["edge_id"].tolist() == ["observed"]


def test_parser_handles_xml_with_no_edges(tmp_path):
    xml_file = tmp_path / "empty.xml"
    xml_file.write_text(
        """
        <meandata>
            <interval begin="0" end="3600"/>
        </meandata>
        """,
        encoding="utf-8",
    )

    df = parse_edge_data(xml_file)

    assert df.empty
    assert "edge_id" in df.columns
    assert "sampled_seconds" in df.columns
    assert "speed" in df.columns


def test_parser_converts_invalid_numeric_values_to_missing(tmp_path):
    xml_file = tmp_path / "edge_data.xml"
    xml_file.write_text(
        """
        <meandata>
            <interval begin="0" end="3600">
                <edge id="edge_1"
                      sampledSeconds="100"
                      speed="invalid"/>
            </interval>
        </meandata>
        """,
        encoding="utf-8",
    )

    df = parse_edge_data(xml_file)

    assert len(df) == 1
    assert pd.isna(df.iloc[0]["speed"])
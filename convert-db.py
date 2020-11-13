import csv


def record_to_filename(record):
    return f"data/{str(record).zfill(4)}.yml"


def split_string(s):
    if s.strip() == "":
        return ["~"]
    if ";" in s:
        return [w.strip() for w in s.split(";")]
    elif "/" in s:
        return [w.strip() for w in s.split("/")]
    else:
        return [s.strip()]


def normalize_usage_label(s):
    s = s.strip()
    if s == "":
        return "~"
    if s == "NA":
        return "~"
    return s


def print_as_yaml_list(string_spreadsheet):
    s = ""
    for line in split_string(string_spreadsheet):
        s += f"  - {line}\n"
    return s


def write_record(row, record):
    tags = "Actionality,Actuality,Additive,Addressee,Apprehension,Assessment,Attitude,Calculation,Caritive,Causation,Cause,Comitative,Comparison,Condition,Concession,Consequence,Degree of accuracy,Degree of intensity,Discourse structure,Epistemic modality (Degree of certainty),Exceptive,Exclusive,Inclusive,Instrument,Manner,Measure,Mirative,Non-existence,Non-Standard Subject,Options,Phase of action,Pluractionality,Possession,Prohibition,Purpose,Quantification,Reaction to the previous discourse,Request,Result,Root modality,Routine,Salient property,Source of information,Source of opinion,Spatial expression,Subset,Taxis,Temporal expression,Temporary characteristics,Timeline,Threat,Volition".split(
        ","
    )

    with open(record_to_filename(record), "w") as f:
        f.write("---\n")
        f.write(f"record: {record}\n")
        f.write(f"name: '{row['Name'].strip()}'\n")
        f.write(f"UD_name: '{row['Name UD'].strip()}'\n")
        f.write(f"illustration: '{row['Illustration'].strip()}'\n")
        f.write(f"cefr_level: A1\n")
        f.write("definitions:\n")
        f.write("  - russian: |\n")
        f.write('        "Example definition in Russian.\n')
        f.write('        It can go over multiple lines."\n')
        f.write("  - english: |\n")
        f.write('        "Example definition in English.\n')
        f.write('        It can go over multiple lines."\n')
        f.write("examples:\n")
        f.write("  - |\n")
        f.write('    "One example.\n')
        f.write('    It can go over multiple lines."\n')
        f.write("  - |\n")
        f.write('    "Another example.\n')
        f.write('    It can go over multiple lines."\n')
        f.write("morphology:\n")
        f.write(print_as_yaml_list(row["Morphology"]))
        f.write("syntactic_function_of_construction:\n")
        f.write(print_as_yaml_list(row["Synt. function of construction"]))
        f.write("syntactic_function_of_anchor:\n")
        f.write(print_as_yaml_list(row["Synt. function of anchor"]))
        f.write("syntactic_structure_of_anchor:\n")
        f.write(print_as_yaml_list(row["Synt. structure of anchor"]))
        f.write("part_of_speech_of_anchor:\n")
        f.write(print_as_yaml_list(row["Part of speech of anchor"]))
        f.write("semantic_roles:\n")
        f.write(print_as_yaml_list(row["Semantic role"]))
        f.write("intonation:\n")
        f.write(
            print_as_yaml_list(
                row["Communicative type (only for Clause and Biclausal)"]
            )
        )
        f.write(f"usage_label: {normalize_usage_label(row['Usage label'])}\n")
        f.write("structure_in_ud: |\n")
        f.write('    "Example structure in UD.\n')
        f.write('    It can go over multiple lines."\n')
        f.write("comment: |\n")
        f.write('    "Example comment.\n')
        f.write('    It can go over multiple lines."\n')
        f.write("semantic_types:\n")
        for tag in tags:
            if row[tag] != "":
                f.write(f"  - type: {tag}\n")
                if row[tag] != "Unspecified":
                    f.write(f"    subptypes:\n")
                    for chunk in row[tag].split(", "):
                        if ":" in chunk:
                            first, second = chunk.split(":")
                            f.write(f"      - type: {first.strip()}\n")
                            f.write(f"        subptypes:\n")
                            f.write(f"          - type: {second.strip()}\n")
                        else:
                            f.write(f"      - type: {chunk.strip()}\n")


if __name__ == "__main__":
    with open("database-2020-10-12.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = int(row["ID Number"])
            write_record(row, record)
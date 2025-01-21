# import codecs.py

# input_file = "C:/datasets/meta-members.csv"
# output_file = "C:/datasets/meta-members-utf8.csv"

# with codecs.open(input_file, "r", "windows-1252") as source_file:
#     with codecs.open(output_file, "w", "utf-8") as target_file:
#         for line in source_file:
#             target_file.write(line)

# import pandas as pd

# # Load the CSV files
# members = pd.read_csv("C:/datasets/meta-members.csv")
# member_to_group = pd.read_csv("C:/datasets/member-to-group-edges.csv")

# # Keep only rows where member_id exists in the members table
# valid_members = set(members["member_id"])
# member_to_group = member_to_group[member_to_group["member_id"].isin(valid_members)]

# # Save the cleaned file
# member_to_group.to_csv("C:/datasets/member-to-group-cleaned.csv", index=False)


# import pandas as pd

# # Load member_edges and members CSV files
# edges = pd.read_csv("C:/datasets/member-edges-cleaned.csv")
# members = pd.read_csv("C:/datasets/meta-members.csv")

# # Filter rows where member1 and member2 exist in members
# valid_ids = set(members["member_id"])
# edges_cleaned = edges[(edges["member1"].isin(valid_ids)) & (edges["member2"].isin(valid_ids))]

# # Save the cleaned file
# edges_cleaned.to_csv("C:/datasets/member-edges-final.csv", index=False)

import pandas as pd

# Load the rsvps and members CSV files
rsvps = pd.read_csv("C:/datasets/rsvps.csv")
members = pd.read_csv("C:/datasets/meta-members.csv")

# Filter rows where member_id exists in the members table
valid_ids = set(members["member_id"])
rsvps_cleaned = rsvps[rsvps["member_id"].isin(valid_ids)]

# Save the cleaned file
rsvps_cleaned.to_csv("C:/datasets/rsvps-cleaned.csv", index=False)

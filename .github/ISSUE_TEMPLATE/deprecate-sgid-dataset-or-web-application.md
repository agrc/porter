---
name: Removing Data From Anywhere
about: Deprecation Checklist
title: Remove <web app/dataset name> from <place>
labels: "deprecation"
assignees: ""
---

# Summary

A short summary of the situation...

<!--
1. The three teams will triage the request, striking through any line that does not apply.
1. Assign each step to someone based on list of assignments
1. All checkboxes should either be removed or checked before closing the issue.
-->

# Triage

- [ ] Data Team Triage (@gregbunce)
- [ ] Dev Team Triage (@steveoh)
- [ ] Cadastre Team Triage (@rkelson)

# Remove data from the following areas

- [ ] ArcGIS Online (assigned to)
- [ ] Internal SGID (assigned to)
- [ ] SGID10 (assigned to)
- [ ] Open SGID (assigned to)
- [ ] Google Drive (assigned to)
- [ ] Open data (assigned to)
- [ ] Mapserv (assigned to)
- [ ] Retire application-specific prod and test SQL Databases (assigned to)

# Copy data to the following areas

- [ ] Upload to UtahAGRC/AGRC_Shelved folder in AGOL (assigned to)
- [ ] Move existing AGOL item to AGRC_Shelved AGOL folder (assigned to)
- [ ] Upload to appropriate UtahAGRC/{SGID Category} folder in AGOL (for "static" datasets) (assigned to)

# Update information in the following areas

- [ ] gis.utah.gov data pages (assigned to)
- [ ] Stewardship doc and sgid-index (assigned to)
- [ ] `SGID.META.AGOLItems` (assigned to)
- [ ] `AGRC_Shelved/AGOLItems_Shelved` (in AGOL) (assigned to)
- [ ] `SGID.META.ChangeDetection` (assigned to)
- [ ] [Backseat Driver](https://github.com/agrc/backseat-driver) (assigned to)

# Is there a website?

- [ ] Archive source code repository (assigned to)
- [ ] Remove from the web server (assigned to)
      or
- [ ] Replace app with a static page with information (assigned to)
      or
- [ ] Redirect somewhere else (assigned to)

# Is there a map service?

- [ ] Stop (assigned to)
- [ ] Delete (assigned to)

# Is there a forklift pallet?

- [ ] Remove repo (assigned to)
- [ ] Remove stale data from forklift hashing and receiving (assigned to)
- [ ] Remove row from `data/hashed/changedetection.gdb/TableHashes`

# Are there service dependencies?

- [ ] Validate that the web api does not query it (assigned to)
- [ ] Validate that AGRC or applications widgets do not reference it (assigned to)

# Notification

- [ ] Blog post (assigned to)
- [ ] Twitter (@steveoh)
  - [ ] Intent
  - [ ] Completed

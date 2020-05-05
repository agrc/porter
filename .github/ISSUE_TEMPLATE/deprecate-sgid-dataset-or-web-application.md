---
name: Removing Data From Anywhere
about: Deprecation Checklist
title: Remove <web app/dataset name> from <place>
labels: 'deprecation'
assignees: ''

---
# Summary

A short summary of the situation...

<!-- 
1. The three teams will triage the request, striking through any line that does not apply.
1. Assign each step to someone based on list of assignments
1. All checkboxes should either be removed or checked before closing the issue.
-->

# Triage

- [ ] Data Team Triage (assigned to)
- [ ] Dev Team Triage (assigned to)
- [ ] Cadastre Team Triage

# Remove data from the following areas

- [ ] ArcGIS Online (assigned to)
- [ ] Internal SGID (assigned to)
- [ ] SGID10 (assigned to)
- [ ] Open SGID (assigned to)
- [ ] Google Drive (assigned to)
- [ ] Open data (assigned to)
- [ ] Mapserv (assigned to)
- [ ] gis.utah.gov data pages (assigned to)
- [ ] Stewardship doc and sgid-index (assigned to)
- [ ] `SGID.META.AGOLItems` (assigned to)
- [ ] `SGID.META.ChangeDetection` (assigned to)

# Copy data to the following areas

- [ ] Upload to UtahAGRC/AGRC_Shelved folder in AGOL (assigned to)
- [ ] Upload to appropriate UtahAGRC/{SGID Category} folder in AGOL (for "static" datasets) (assigned to)

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

# Are there service dependencies?

- [ ] Validate that the web api does not query it (assigned to)
- [ ] Validate that AGRC or applications widgets do not reference it (assigned to)

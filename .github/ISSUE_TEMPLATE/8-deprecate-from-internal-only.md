---
name: (🔐 UGRC internal use) Internal/Open SGID only deprecation
about: Data is being removed from Internal/Open SGID but preserved in AGOL.
title: Remove <thing> from Internal/Open SGID while preserving in AGOL
labels: "deprecation, porter"
assignees: "@stdavis, @eneemann, @rkelson"
---

## Summary

<!-- conductor = {"table":""} -->

- **Internal Dataset Name**: SGID.<category>.<dataset>
- **External Dataset Name**:
- **ArcGIS Online Url**:

_A short summary of the situation._

### Migration Guide

_A short summary of how users affected by this deprecation can modify their workflows and projects to continue to get similar or improved functionality_

<!-- this is here to help the writing juices flow. feel free to completely replace this or simply fill in the blanks -->

This dataset has been removed from internal and Open SGID but can still be access in the SGID on ArcGIS.

### Action items

1. _Assign a person who should complete the task by replacing `name` with their github `@name`._
1. _Check [x] the box when the task is completed and add the date of completion._
1. _~Strike~ out all items that do not apply._

- [ ] Move entry from SGID.META.AGOLItems to AGOLItems_shelved in AGOL (name, completed: `2026/00/00`)
  - [ ] For datasets that will continue to be updated and only live in AGOL, leave the `CATEGORY` field blank. Auditor will split the tablename to determine the category.
  - [ ] For datasets that are not being updated and should only live in AGOL, set `CATEGORY` to `static`. Auditor will set the category/folder/thumbnail according to the category in the tablename and add both a `static` tag and a note in the description about it continuing to be part of the SGID.
  - [ ] For datasets that have been superseded by a newer version but should still be kept for historical reference (like previous census or tax area data), set `CATEGORY` to `shelved`. Auditor will move the dataset to the UGRC Shelf folder and group and add a note in the description.
- [ ] Update the [SGID Index](https://docs.google.com/spreadsheets/d/11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ/edit#gid=1024261148) update "storageType" to be "AGOL". (name, completed: `2026/00/00`)
- [ ] Check if this layer in the base maps. If so, work with Zach to develop a path forward before you proceed with a Hard Delete (name, completed: `2026/00/00`).
- [ ] Add "Backup" tag to AGOL Item so that it is backed up by [Moonwalk](https://github.com/agrc/project-moonwalk) (name, completed: `2026/00/00`)
- [ ] Manually remove data from the Internal SGID (name, completed: `2026/00/00`)
- [ ] Remove Farm from AGOL connection (forklift) (name, completed: `2026/00/00`)
- [ ] Update relevant [gis.utah.gov](https://gis.utah.gov/products/sgid/categories/) product pages (including `downloadMetadata.ts` and `public/_redirects`) (name , completed: `2026/00/00`)
- [ ] Delete [Google Drive](https://drive.google.com/drive/folders/0ByStJjVZ7c7mNlZRd2ZYOUdyX2M) data (name, completed: `2026/00/00`)
- [ ] Remove row from `SGID.META.ChangeDetection` (name, completed: `2026/00/00`) (it was already gone)
- [ ] Remove data from forklift hashing and receiving (name, completed: `2026/00/00`)
- [ ] Remove row from `data/hashed/changedetection.gdb/TableHashes` (name, completed: `2026/00/00`)
- [ ] Remove data from record series with archives (name, completed: `2026/00/00`)

### :robot: Automation validation

1. _Assign yourself or someone to check the item by replacing `name` with their github `@name`._
1. _Check [ ] the box and add the date of verification `2026/01/01` when the task is verified._
1. _~Strike~ out all items that do not apply._

- [ ] Remove data from Open SGID (name on `2026/00/00`)
- [ ] [sgid-index](https://gis.utah.gov/products/sgid/sgid-index/) (name on `2026/00/00`)
- [ ] Auditor sets appropriate category information (including `shelved`/`static` info as needed as well as moving to appropriate folders and groups) (name on `2026/00/00`)

### Are there service dependencies

- [ ] Are clients querying this data with the UGRC API search endpoint? [This dashboard](https://lookerstudio.google.com/reporting/fbfcf1d5-e9c2-4b8a-94ae-9529d5d0bbef/page/p_7k74ao7wjd) may be helpful.
- [ ] Notify Don Jackson (don.jackson1 at motorolasolutions.com) if the data is in the Next-Generation 911 Motorola Aware Map? (name on `2026/00/00`)
- [ ] Does any other application depend on this data? (name on `2026/00/00`)
  - dependency 1

### Notification

- [ ] X (@stdavis)

### Group Task Assignments

1. _Check [ ] the box when you have assigned all the tasks relevant to your group._

- [ ] Data Team (@eneemann)
- [ ] Dev Team (@stdavis)
- [ ] Cadastre Team (@rkelson)

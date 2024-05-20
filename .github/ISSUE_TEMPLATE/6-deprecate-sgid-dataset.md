---
name: (🔐 UGRC internal use) SGID deprecation
about: SGID data is no longer relevant or has been replaced
title: Remove <dataset name> from SGID
labels: "deprecation, porter"
assignees: "@steveoh, @gregbunce, @rkelson"
---

## Summary

<!-- conductor = {"table":"category.internaltablename"} -->

- **Internal Dataset Name**:
- **External Dataset Name**:
- **ArcGIS Online Url**:

_A short summary of the situation._

### Migration Guide

_A short summary of how users affected by this deprecation can modify their workflows and projects to continue to get similar or improved functionality_

<!-- this is here to help the writing juices flow. feel free to completely replace this or simply fill in the blanks -->

This dataset has been replaced by () which is named () in the Open SGID and () in the SGID on ArcGIS.
The replaced data is still accessible via our shelved policy in AGOL (a link to the shelved item).

### Action items

1. _Assign a person who should complete the task by replacing `name` with their github `@name`._
1. _Check [x] the box when the task is completed and add the date of completion._
1. _~Strike~ out all items that do not apply._

#### Soft Delete

_The purpose of the soft delete is to ensure that all of our users and applications have gracefully migrated off of the dataset. Soft deletes will remain in effect for 14 days. During this time, we will have the ability to restore the dataset to its original SGID offering(s). After these 14 days, the item is then ready for a hard delete._

Note: If this dataset is being replaced, then wait until the new data is publicly available before completing these steps:

- [ ] Append "(Mature Support)" to the end of the item title in the `SGID.META.AGOLItems` table (name, completed: `2024/00/00`)
- [ ] Remove all tags other than "Deprecated" in the SDE metadata (name, completed: `2024/00/00`)
- [ ] Add note to SDE description noting when layer will be deleted and any replacement layer (name, completed: `2024/00/00`)
- [ ] Update the [SGID Index](https://docs.google.com/spreadsheets/d/11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ/edit#gid=1024261148) row as deprecated by pasting the related Porter issue URL in the "porterUrl" field and setting the value of the "ugrcStatus" field as "removed". Also update the "refreshCycle" field (name, completed: `2024/00/00`)
- [ ] Change `Authoritative` field to `d` in `SGID.META.AGOLItems` to automatically set the `Deprecated` AGOL flag. Allow the `d` to persist through one run of [Auditor](https://github.com/agrc/auditor) - currently, Auditor runs daily at 5:00am (name, completed: `2024/00/00`)
  - After at least one successful run of Auditor:
    - [ ] Remove the row from the `SGID.META.AGOLItems` table. This will trigger the removal of this item in Open SGID (name, completed: `2024/00/00`)
    - [ ] Unshare the item from its SGID group, which will remove it from the SGID on ArcGIS (name, completed: `2024/00/00`)
- [ ] Check if this layer in the base maps. If so, work with Zach to develop a path forward before you proceed with a Hard Delete (name, completed: `2024/00/00`).

#### Hard Delete

**Target Date:** 2024/00/00

_Hard deletes are final. It is recommended to complete the soft delete process before moving on to these steps. If you decide to skip the soft delete, note that you will need to incorporate some of those steps here._

- [ ] Manually remove data from the Internal SGID (name, completed: `2024/00/00`)
  - [ ] Deprecated database layers should be backed up on Google Drive > AGRC Projects > SGID > deprecated layers > [internal_db_sgid_layers](https://drive.google.com/drive/u/0/folders/10Fk8NI2UpEUnAbgvhjlN18pyvSFDWyIq) (name, completed: `2024/00/00`).
- [ ] Remove ArcGIS Online item: (name, completed: `2024/00/00`)
  - Manually delete the AGOL item
  - -OR-
  - Unshare by changing the `AGOL_ITEM_ID` field in `SGID.META.AGOLItems` to something other than an Item ID and manually changing the sharing settings (remove the item from all SGID groups, remove Public sharing),
  - -OR-
  - Shelve the data by copying the row from `SGID.META.AGOLItems` to the `AGOLItems_shelved` table in AGOL and changing the `AGOL_ITEM_ID` field in `SGID.META.AGOLItems` to `shelved` or some other note.
  - Deprecated AGOL items can be backed up on Google Drive > AGRC Projects > SGID > deprecated layers > [agol_sgid_layers](https://drive.google.com/drive/u/0/folders/1xwSxiDNIH-9Hhmn6I7NfKBhm4SbYonX5).
- [ ] Remove Farm from AGOL connection (name, completed: `2024/00/00`)
- [ ] Update the [SGID Index](https://docs.google.com/spreadsheets/d/11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ/edit#gid=1024261148) fields: "arcGisOnline", "openSgid", "openSgidTableName"
- [ ] Update relevant [gis.utah.gov](https://gis.utah.gov/data) data pages (including `downloadMetadata.ts`) (name, completed: `2024/00/00`)
- [ ] Update `SGID.META.AGOLItems` table (name, completed: `2024/00/00`)
  - cut and paste row to `AGOLItems_shelved` table if shelving (see below)
  - set the `AGOL_ITEM_ID` field to `hosted by <agency>` for Farm from AGOL
  - set the `AGOL_ITEM_ID` field to `exclude from AGOL` to not publish to ArcGIS Online
- [ ] Delete Google Drive data (name, completed: `2024/00/00`)
- [ ] Remove row from `SGID.META.ChangeDetection` (name, completed: `2024/00/00`)
- [ ] Remove data from forklift hashing and receiving (name, completed: `2024/00/00`)
- [ ] Remove row from `data/hashed/changedetection.gdb/TableHashes` (name, completed: `2024/00/00`)

#### Shelve/Static

_Choose one based on situation._

- [ ] Upload to `UtahAGRC/AGRC_Shelved` folder in AGOL (New shelved item not already in AGOL) (name, completed: `2024/00/00`)
- [ ] Move existing AGOL item to `AGRC_Shelved` AGOL folder (shelving an item already in AGOL) (name, completed: `2024/00/00`)
- [ ] Upload to appropriate `UtahAGRC/{SGID Category}` folder in AGOL (for `static` datasets) (name, completed: `2024/00/00`)

_Add record to table._

- [ ] Add record to `AGOLItems_shelved` [table](https://utah.maps.arcgis.com/home/item.html?id=1760fbedbc7e49429aa6c0c3ab1442ec) in ArcGIS Online with `shelved` or `static` in the `CATEGORY` field (name, completed: `2024/00/00`)

### :robot: Automation validation

1. _Assign yourself or someone to check the item by replacing `name` with their github `@name`._
1. _Check [x] the box and add the date of verification `2020/01/01` when the task is verified._
1. _~Strike~ out all items that do not apply._

- [ ] Remove data from Open SGID (name on `2024/00/00`)
- [ ] [sgid-index](https://gis.utah.gov/data/sgid-index) (@steveoh on `2024/00/00`)
- [ ] Auditor sets appropriate `shelved`/`static`/`Deprecated` information (@jacobdadams on `2024/00/00`)

### Are there service dependencies

- [ ] Are clients querying this data with the WebAPI?
- [ ] Notify Don Jackson (don.jackson1 at motorolasolutions.com) if the data is in the Next-Generation 911 Motorola Aware Map? (@gregbunce on `2024/00/00`)
- [ ] Does any other application depend on this data?

### Notification

- [ ] Twitter (@steveoh)

### Group Task Assignments

1. _Check [x] the box when you have assigned all the tasks relevant to your group._

- [ ] Data Team (@gregbunce)
- [ ] Dev Team (@steveoh)
- [ ] Cadastre Team (@rkelson)

---
name: Introduce data to the SGID
about: Creation Checklist
title: Add <dataset name> from <place>
labels: "introduction, porter"
assignees: ""
---

<!--
Introduce your data, where it comes from, why it is being added etc
-->

# Summary

- **Proposed Dataset Name**: Foo
- **Proposed ArcGIS Online Name**: Utah Foo
- **Proposed ISO Category**: Quux
- **Data Description**: Bar
- **Source Agency/Entity**: Baz
- **Contact**: Bar Baz
- **Update Frequency**: Quarterly

<!--
When the champion from your team has completed the triage, check [x] the checkbox
-->

# Triage

- [ ] Data Team Triage (@gregbunce)
- [ ] Dev Team Triage (@steveoh)
- [ ] Cadastre Team Triage (@rkelson)

# We are introducing data

The data was or will be added on `2020/00/00` to the following areas

<!--
add an [x] to the applicable areas you plan to add the data or ~strike~ out thoses that do not apply.
If adding to the internal SGID with the hopes that swapper and forklift will push the item to SGID10 and AGOL
you can strike them out. They are available if for some reason the internal sgid is skipped.
-->

- [ ] Internal SGID
- [ ] SGID10
- [ ] ArcGIS Online

<!--
the data should be in good shape.
-->

# The data is high quality

- [ ] Sweeper checks have run and passed
- [ ] The minimum requirements for [metadata](https://gis.utah.gov/about/policy/sgid/) are populated
- [ ] The data complies with our [domain rules](https://gis.utah.gov/about/policy/sgid/)

<!--
Where do we expect the data to show up. Check [x] all the areas
-->

# The data should propagate automatically to

- [ ] ArcGIS Online
- [ ] Internal SGID (assigned to)
- [ ] Open SGID
- [ ] Open Data
- [ ] `SGID.META.ChangeDetection`

# References to the data need to be manually added to

- [ ] gis.utah.gov data pages
- [ ] [Stewardship doc](https://docs.google.com/spreadsheets/d/11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ/edit#gid=1)
- [ ] `SGID.META.AGOLItems`
- [ ] `AGOLItems_shelved` [metatable](http://utah.maps.arcgis.com/home/item.html?id=1760fbedbc7e49429aa6c0c3ab1442ec) (AGOL version of the metatable for any `static` or `shelved` items)

<!--
assign yourself or someone to check that the dataset is live in its area. once verified, add the date of verification `2020/01/01`
-->

# We have verified the data is live

- [ ] ArcGIS Online (@assigned on ``)
- [ ] Internal SGID (@assigned on ``)
- [ ] Open SGID (@assigned on ``)
- [ ] [Open data](https://opendata.gis.utah.gov) (@assigned on ``)
- [ ] gis.utah.gov data pages (@assigned on ``)
- [ ] [sgid-index](https://gis.utah.gov/data/sgid-index) (@assigned on ``)
- [ ] `SGID.META.AGOLItems` (@assigned on ``)
- [ ] `SGID.META.ChangeDetection` (@assigned on ``)
- [ ] [agol-validator](https://github.com/agrc/agol-validator) items (@assgined on ``)

# Notification

- [ ] Blog post (@assigned)
- [ ] Twitter (@steveoh)

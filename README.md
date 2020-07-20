# Porter

A porter is person that

- carries things, such as bags
- performs routine cleaning, likely on a train, taking care of the sleeping berths.

AGRC tracks the additions, replacements, and deletions of SGID items (in the broadest sense of add, replace, or delete) through issues in this repository.

## How to use

1. [Create a new issue](https://github.com/agrc/cemetery/issues/new/choose) when an application, dataset, or both needs to be added, deleted, or moved to a different long-term storage
1. Choose the `Removing Data From Anywhere` (for moving or deleting data) or `Introduce data to the SGID` (for adding data) template from the buttons
1. Tag the three triagers (one from each team) in the triage section:
   - [ ] Data Team Triage (@gregbunce)
1. The triagers will choose which items need to be handled and tag the appropriate people to handle them:
   - [ ] ArcGIS Online (@jacobdadams)
   - Items that don't need to be handled should be struck through (wrap the line with `~`'s) instead of being deleted:
      - `~ArcGISOnline (assigned to)~` (note there are no spaces between the `~`'s and the text to be struck out)
   - Once the triager has identified any steps required for their team or made any relevant comments, they should check the box in the triage section to indicate that their triage is complete:
      - [x] Data Team Triage (@gregbunce)
1. The people assigned to different issues will check the boxes as they are completed and comment on the issue to notify the rest of the group:
   - [x] ArcGIS Online (@jacobdadams)
1. Once all boxes are checked, the person who first opened the issue should close it.

## Data Flow for New SGID Datasets

Data in the internal SGID will automatically be added to the SGID10 with via the swapper pallet.

If there is a record added to `SGID.META.AGOLItems`, the corresponding dataset will automatically be added to:

1. the open sgid with cloudb
1. arcgis online with forklift
1. open data with the agol validator

Note: Cloudb is the only automation from the list above works in reverse. If a record is removed from `SGID.META.AGOLItems`, the corresponding data needs to be manually removed from all of the systems above with the exception of the Open SGID.

### Tweet templates

#### intent to deprecate

```md
🚮🗑️🚮 Deprecation Notice 🚮🗑️🚮

[Dataset]

https://github.com/agrc/porter/issues/#

#utmap #agrcporter
```

#### issue completed

```md
🚮🗑️🚮 Deprecation Complete 🚮🗑️🚮

[Dataset]

https://github.com/agrc/porter/issues/#

#utmap #agrcporter
```

#### intent to add

```md

🌱🌱The SGID is getting larger🌳🌳

Dataset from Agency coming soon!

https://github.com/agrc/porter/issues/#

Follow along and comment if you are interested!

#utmap #agrcporter
```

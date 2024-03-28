# Changelog

## [2.4.2](https://github.com/agrc/porter/compare/v2.4.1...v2.4.2) (2024-03-28)


### 🐛 Bug Fixes

* updates for new sgid index ([7d68ebb](https://github.com/agrc/porter/commit/7d68ebb7c6d16b4319ab7ef266017cbd1730577a))

## [2.4.1](https://github.com/agrc/porter/compare/v2.4.0...v2.4.1) (2023-10-13)


### 🌲 Dependencies

* bump the major-dependencies group with 1 update ([acb18ee](https://github.com/agrc/porter/commit/acb18eefe074439cb17858ce3066b5d4be300f85))

## [2.4.0](https://github.com/agrc/porter/compare/v2.3.0...v2.4.0) (2023-10-13)


### 🚀 Features

* 2023 update  ([ea46eab](https://github.com/agrc/porter/commit/ea46eab788c777cb684a73734477269099b850f0))


### 🐛 Bug Fixes

* add missing analytics cleanup step ([2aa080d](https://github.com/agrc/porter/commit/2aa080d406cf928d8427894249328a46b811878e))


### 🌲 Dependencies

* 2023 Q4 updates ([20a85e5](https://github.com/agrc/porter/commit/20a85e54c99699d0f857f4d61270d4b3d183b6f6))
* update flask to 3 to match cloud run requirements ([ea70432](https://github.com/agrc/porter/commit/ea70432ec49cbc077178c026c90e7a183b2cfa70))


### 📖 Documentation Improvements

* add note about agol item id field ([4d830aa](https://github.com/agrc/porter/commit/4d830aabb12eb0286d154647b2fb8c75f71dfabe))

## [2.3.0](https://github.com/agrc/porter/compare/v2.1.1...v2.3.0) (2023-06-28)


### 🚀 Features

* add action item for APM in ServiceNow ([0e9aa63](https://github.com/agrc/porter/commit/0e9aa6347e6ca4a43505f2f89702241cd4fd5273))
* add introduce application template ([cc19f28](https://github.com/agrc/porter/commit/cc19f2874a9f789f9abfa1e91d35de6bc3821aec)), closes [#212](https://github.com/agrc/porter/issues/212)
* add NG911 check for deprecation template ([a434fe6](https://github.com/agrc/porter/commit/a434fe696ff65b1a44f7395df67209d05200caf5))
* add prod and dev deploy jobs ([6de264f](https://github.com/agrc/porter/commit/6de264fa74cd1253dd52f5344a4a9c6aee396244))
* add quad word removal step ([755d353](https://github.com/agrc/porter/commit/755d35352e62d362845970a3ae60ea892c4d2450))
* add step for unregistering data stores in arcgis server ([7f7c59c](https://github.com/agrc/porter/commit/7f7c59c9191073a9457b2fe60c8c8368921ffcdb))
* incorporate ideas from recent AGOL blog post ([d39f6ed](https://github.com/agrc/porter/commit/d39f6ed6ba43ed5dbc3689aede5d6598555e8950))
* read configuration status from environment variable ([2126733](https://github.com/agrc/porter/commit/21267334f65c819531ecf1f4b390b54fd21cb842))


### 🌲 Dependencies

* update dependencies, switch to black, ruff, and pyproject ([5e77668](https://github.com/agrc/porter/commit/5e776680737e3866915785fa32ae2837cd0b6f19))


### 🎨 Design Improvements

* format with new tools ([543c6ac](https://github.com/agrc/porter/commit/543c6ac3877cbf17a8d310ade7d0c8f0751d4f05))


### 📖 Documentation Improvements

* agrc -&gt; ugrc ([484ae29](https://github.com/agrc/porter/commit/484ae2901bfb7d14be09c6943558a4cbd7d722bf))
* agrc -&gt; ugrc ([8eb2ae4](https://github.com/agrc/porter/commit/8eb2ae4211068748b4b717bd4e912f9daefb631f))
* update readme's ([e1f7bb9](https://github.com/agrc/porter/commit/e1f7bb97441ebd8fbab5cfd434700094083a2e4a))
* update twitter stuff ([d8bd236](https://github.com/agrc/porter/commit/d8bd2362e7b0cb7d40b2aedfc17cdda63a388816))


### 🐛 Bug Fixes

* **action:** add full version back ([60c7ddb](https://github.com/agrc/porter/commit/60c7ddb647a192fd281da15d01001311b5e92476))
* add missing assignment tags ([af3895a](https://github.com/agrc/porter/commit/af3895a2948883a7c9152e4d4a4ef25fbdc6b5c7))
* add missing timeout input ([8d99293](https://github.com/agrc/porter/commit/8d9929318e344ed29e23e09822bbaa9b5322c9fb))
* add reminder about packing slip update ([fac8353](https://github.com/agrc/porter/commit/fac8353a423f287b54b430a001ce182d96bdbadb))
* add sub-headings to application urls for dev and prod ([0ad58a1](https://github.com/agrc/porter/commit/0ad58a10e877b523c481e1482dc1ceb682b170ab))
* **ci:** allow environment variables to flow into cloud run ([ae56332](https://github.com/agrc/porter/commit/ae5633222d99d0e8aee170f520d3125a6ffc1985))
* **ci:** correct registry url ([8d9a835](https://github.com/agrc/porter/commit/8d9a8352c35b38d9b26d7cd2d85d967099ead4d7))
* **ci:** least privilege ([c82b7a1](https://github.com/agrc/porter/commit/c82b7a1496c6677fd336019bc17fd478b51554e7))
* **ci:** least privilege ([4bfbc20](https://github.com/agrc/porter/commit/4bfbc20b9400fe835022a2f596953cbfb333b466))
* **ci:** update spelling and token format ([387ec17](https://github.com/agrc/porter/commit/387ec17011dd8312822f33a17e869b0d23b3a485))
* clarify where soft delete steps should be made ([7075fd0](https://github.com/agrc/porter/commit/7075fd01cb4bfc6e4078b7ceb8cfcd05b65a9d75))
* correct pytest configuration ([8e76e63](https://github.com/agrc/porter/commit/8e76e6390d2fa0674b78bd1d9827dc126748279f))
* correct secret access for gsheets ([28ba5bb](https://github.com/agrc/porter/commit/28ba5bb4e3895405489abc5166be747ee56c94e8))
* create placeholders for results of tasks ([f3445f9](https://github.com/agrc/porter/commit/f3445f9df831952fc473b05d013129be94c779c0))
* json load sa data ([3ab907f](https://github.com/agrc/porter/commit/3ab907f777ac60ba09e46af4cbc2bed91df05c71))
* point at versioned view of meta table ([a835a51](https://github.com/agrc/porter/commit/a835a518de048c25c248c10b36adeea52980f9e9))
* remove duplicate task ([acae6f8](https://github.com/agrc/porter/commit/acae6f8356ded01f80f17f3741ebf8e332982a2d))
* remove impossible task ([d99adcb](https://github.com/agrc/porter/commit/d99adcb373665cdf295d02412b5ff63202ff0bab))
* remove unnecessary quotes ([3c97362](https://github.com/agrc/porter/commit/3c97362c9f2b23f27bb51e824cf233820dc8ac1d))
* set nathan as default assignment ([45afbd0](https://github.com/agrc/porter/commit/45afbd058b549327b2c59a91be37f9a414a6fa31))
* set nathan as initial assignee ([870d642](https://github.com/agrc/porter/commit/870d6420d37086c050d243145483b30e66eb05de))
* update default year to 2022 ([921d248](https://github.com/agrc/porter/commit/921d2487bfdd2bcf8e6347612ee0a7aa43ef5cd2))
* update release ci pipeline ([249dc75](https://github.com/agrc/porter/commit/249dc753c8d8e6156f66578c85beae6d08e50c31))
* use less-confusing word ([1fb26dd](https://github.com/agrc/porter/commit/1fb26dd32ab57a8b3a6c6e7a1384c59c3812e7c8))
* use single curlies and quote env variable with different separator ([977d38b](https://github.com/agrc/porter/commit/977d38bb28eef0a5e32d11e13edf8861c99cc7da))

## [2.3.0-6](https://github.com/agrc/porter/compare/v2.3.0-5...v2.3.0-6) (2023-06-27)


### 🐛 Bug Fixes

* correct pytest configuration ([9d7c1a7](https://github.com/agrc/porter/commit/9d7c1a7a4f305b9b08c67f2f60a1e6603bfe71b1))

## [2.3.0-5](https://github.com/agrc/porter/compare/v2.3.0-4...v2.3.0-5) (2023-06-27)


### 🐛 Bug Fixes

* **ci:** allow environment variables to flow into cloud run ([4119b3f](https://github.com/agrc/porter/commit/4119b3f50c13cb778c74da177b3c16409ff91ddb))

## [2.3.0-4](https://github.com/agrc/porter/compare/v2.3.0-3...v2.3.0-4) (2023-06-27)


### 🐛 Bug Fixes

* **ci:** least privilege ([3f2e92d](https://github.com/agrc/porter/commit/3f2e92df8a85d36c7c4fc698f4594ab59b7d410c))

## [2.3.0-3](https://github.com/agrc/porter/compare/v2.3.0-2...v2.3.0-3) (2023-06-27)


### 🐛 Bug Fixes

* **ci:** least privilege ([fea56e5](https://github.com/agrc/porter/commit/fea56e5113aa6a5be4f37d173ad04c2fc0e72540))

## [2.3.0-2](https://github.com/agrc/porter/compare/v2.3.0-1...v2.3.0-2) (2023-06-27)


### 🐛 Bug Fixes

* **ci:** correct registry url ([e51f97f](https://github.com/agrc/porter/commit/e51f97f6664e97bc42a5a22f567ea797525210e1))

## [2.3.0-1](https://github.com/agrc/porter/compare/v2.3.0-0...v2.3.0-1) (2023-06-27)


### 🐛 Bug Fixes

* **ci:** update spelling and token format ([cdc77f1](https://github.com/agrc/porter/commit/cdc77f1df6c28525a3948ece058a486a88570d82))

## [2.3.0-0](https://github.com/agrc/porter/compare/v2.1.1...v2.3.0-0) (2023-06-27)


### 🚀 Features

* add action item for APM in ServiceNow ([0e9aa63](https://github.com/agrc/porter/commit/0e9aa6347e6ca4a43505f2f89702241cd4fd5273))
* add introduce application template ([cc19f28](https://github.com/agrc/porter/commit/cc19f2874a9f789f9abfa1e91d35de6bc3821aec)), closes [#212](https://github.com/agrc/porter/issues/212)
* add NG911 check for deprecation template ([a434fe6](https://github.com/agrc/porter/commit/a434fe696ff65b1a44f7395df67209d05200caf5))
* add prod and dev deploy jobs ([6de264f](https://github.com/agrc/porter/commit/6de264fa74cd1253dd52f5344a4a9c6aee396244))
* add quad word removal step ([755d353](https://github.com/agrc/porter/commit/755d35352e62d362845970a3ae60ea892c4d2450))
* add step for unregistering data stores in arcgis server ([7f7c59c](https://github.com/agrc/porter/commit/7f7c59c9191073a9457b2fe60c8c8368921ffcdb))
* incorporate ideas from recent AGOL blog post ([d39f6ed](https://github.com/agrc/porter/commit/d39f6ed6ba43ed5dbc3689aede5d6598555e8950))
* read configuration status from environment variable ([2126733](https://github.com/agrc/porter/commit/21267334f65c819531ecf1f4b390b54fd21cb842))


### 🌲 Dependencies

* update dependencies, switch to black, ruff, and pyproject ([03b003b](https://github.com/agrc/porter/commit/03b003bb8f478aa0e4dda92da6a1847a6e199806))


### 🎨 Design Improvements

* format with new tools ([418eab3](https://github.com/agrc/porter/commit/418eab3a645a3d7a887d48d15cd1e07088facd69))


### 📖 Documentation Improvements

* agrc -&gt; ugrc ([484ae29](https://github.com/agrc/porter/commit/484ae2901bfb7d14be09c6943558a4cbd7d722bf))
* agrc -&gt; ugrc ([8eb2ae4](https://github.com/agrc/porter/commit/8eb2ae4211068748b4b717bd4e912f9daefb631f))
* update readme's ([fccada0](https://github.com/agrc/porter/commit/fccada0f09ac503e3f9bb6621d5bc452d38d291d))
* update twitter stuff ([d8bd236](https://github.com/agrc/porter/commit/d8bd2362e7b0cb7d40b2aedfc17cdda63a388816))


### 🐛 Bug Fixes

* **action:** add full version back ([60c7ddb](https://github.com/agrc/porter/commit/60c7ddb647a192fd281da15d01001311b5e92476))
* add missing assignment tags ([af3895a](https://github.com/agrc/porter/commit/af3895a2948883a7c9152e4d4a4ef25fbdc6b5c7))
* add missing timeout input ([8d99293](https://github.com/agrc/porter/commit/8d9929318e344ed29e23e09822bbaa9b5322c9fb))
* add reminder about packing slip update ([fac8353](https://github.com/agrc/porter/commit/fac8353a423f287b54b430a001ce182d96bdbadb))
* add sub-headings to application urls for dev and prod ([0ad58a1](https://github.com/agrc/porter/commit/0ad58a10e877b523c481e1482dc1ceb682b170ab))
* clarify where soft delete steps should be made ([7075fd0](https://github.com/agrc/porter/commit/7075fd01cb4bfc6e4078b7ceb8cfcd05b65a9d75))
* correct secret access for gsheets ([28ba5bb](https://github.com/agrc/porter/commit/28ba5bb4e3895405489abc5166be747ee56c94e8))
* create placeholders for results of tasks ([f3445f9](https://github.com/agrc/porter/commit/f3445f9df831952fc473b05d013129be94c779c0))
* json load sa data ([3ab907f](https://github.com/agrc/porter/commit/3ab907f777ac60ba09e46af4cbc2bed91df05c71))
* point at versioned view of meta table ([a835a51](https://github.com/agrc/porter/commit/a835a518de048c25c248c10b36adeea52980f9e9))
* remove duplicate task ([acae6f8](https://github.com/agrc/porter/commit/acae6f8356ded01f80f17f3741ebf8e332982a2d))
* remove impossible task ([d99adcb](https://github.com/agrc/porter/commit/d99adcb373665cdf295d02412b5ff63202ff0bab))
* remove unnecessary quotes ([3c97362](https://github.com/agrc/porter/commit/3c97362c9f2b23f27bb51e824cf233820dc8ac1d))
* set nathan as default assignment ([45afbd0](https://github.com/agrc/porter/commit/45afbd058b549327b2c59a91be37f9a414a6fa31))
* set nathan as initial assignee ([870d642](https://github.com/agrc/porter/commit/870d6420d37086c050d243145483b30e66eb05de))
* update default year to 2022 ([921d248](https://github.com/agrc/porter/commit/921d2487bfdd2bcf8e6347612ee0a7aa43ef5cd2))
* update release ci pipeline ([86d4993](https://github.com/agrc/porter/commit/86d4993d51d1c82e44ccd24f131b7f939b2f343c))
* use less-confusing word ([1fb26dd](https://github.com/agrc/porter/commit/1fb26dd32ab57a8b3a6c6e7a1384c59c3812e7c8))
* use single curlies and quote env variable with different separator ([977d38b](https://github.com/agrc/porter/commit/977d38bb28eef0a5e32d11e13edf8861c99cc7da))

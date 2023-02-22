# Changelog

## Table of contents

- [2.1.1](#211)
- [2.1.0](#210)
- [2.0.0](#200)
- [1.0.1](#101)
- [1.0.0](#100)

## 2.1.1

### Fixes

- Fix `FieldConverter`s not being handled correctly in `create_template_from_model`

## 2.1.0

### Features

- Add `create_template_from_model` to generate template dicts from models with required fields

### Changes

- Reorganize helpers into modules inside a `helpers` package

### Code

- Add unit tests for `create_template_from_model`
- Add unit tests for `FieldConverter`
- Add GitHub action to run unit tests

## 2.0.0

### Changes

- Git ignore `.python-version`

### Compatibility

- Raise Python requirement to `^3.7` (breaking -- dependency compatibility issues I hadn't tested)
- Fix parameterized types for Python `<3.9`

## 1.0.1

### Fixes

- Fix missing dependencies
- Fix incorrect import name
- Fix optional imports not actually being optional
- Fix converter logic failing due to name collision

### Compatibility

- Lower Python requirement to `^3.6`

## 1.0.0

### Features

- Initial functionality

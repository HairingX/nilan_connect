---
name: Bug / problem report
about: Report a problem so we can improve the integration
title: ''
labels:
assignees: HairingX

---

**Describe the bug or problem (In Danish is OK)**
<!--
  A clear and concise description of what the bug or problem is.
-->

**Please answer the following**
- Version of integration:
- Version of Home Assistant:
- [ ] I have more than one child
- [ ] My children are attending different schools / institutions

**REQUIRED! Provide debug log from the integration**
- Enable by adding the following to your configuration.yaml:
```
logger:
  default: info
  logs:
    custom_components.nilan_connect: debug
```
- Restart Home Assistant
- Capture all log lines (from the integration only), save it to a file and attach it to here.

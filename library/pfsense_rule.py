#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Orion Poplawski <orion@nwra.com>
# Copyright: (c) 2018, Frederic Bor <frederic.bor@wanadoo.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: pfsense_rule
version_added: "2.9"
author: Orion Poplawski (@opoplawski), Frederic Bor (@f-bor)
short_description: Manage pfSense rules
description:
  - Manage pfSense rules
notes:
options:
  name:
    description: The name the rule
    required: true
    default: null
    type: str
  action:
    description: The action of the rule
    required: true
    default: pass
    choices: [ "pass", "block", "reject" ]
    type: str
  state:
    description: State in which to leave the rule
    default: present
    choices: [ "present", "absent" ]
    type: str
  disabled:
    description: Is the rule disabled
    default: false
    type: bool
  interface:
    description: The interface for the rule
    required: true
    type: str
  floating:
    description: Is the rule floating
    type: bool
  direction:
    description: Direction floating rule applies to
    choices: [ "any", "in", "out" ]
    type: str
  ipprotocol:
    description: The IP protocol
    default: inet
    choices: [ "inet", "inet46", "inet6" ]
    type: str
  protocol:
    description: The protocol
    default: any
    choices: [ "any", "tcp", "udp", "tcp/udp", "icmp", "igmp" ]
    type: str
  source:
    description: The source address, in [!]{IP,HOST,ALIAS,any,(self)}[:port], IP:INTERFACE or NET:INTERFACE format
    required: true
    default: null
    type: str
  destination:
    description: The destination address, in [!]{IP,HOST,ALIAS,any,(self)}[:port], IP:INTERFACE or NET:INTERFACE format
    required: true
    default: null
    type: str
  log:
    description: Log packets matched by rule
    type: bool
  after:
    description: Rule to go after, or "top"
    type: str
  before:
    description: Rule to go before, or "bottom"
    type: str
  statetype:
    description: State type
    default: keep state
    choices: ["keep state", "sloppy state", "synproxy state", "none"]
    type: str
  queue:
    description: QOS default queue
    type: str
  ackqueue:
    description: QOS acknowledge queue
    type: str
  in_queue:
    description: Limiter queue for traffic coming into the chosen interface
    type: str
  out_queue:
    description: Limiter queue for traffic leaving the chosen interface
    type: str
  gateway:
    description: Leave as 'default' to use the system routing table or choose a gateway to utilize policy based routing.
    type: str
    default: default
"""

EXAMPLES = """
- name: "Add Internal DNS out rule"
  pfsense_rule:
    name: 'Allow Internal DNS traffic out'
    action: pass
    interface: lan
    ipprotocol: inet
    protocol: udp
    source: dns_int
    destination: any:53
    after: 'Allow proxies out'
    state: present
"""

RETURN = """

"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.pfsense.pfsense_rule import PFSenseRuleModule, RULES_ARGUMENT_SPEC, RULES_REQUIRED_IF


def main():
    module = AnsibleModule(
        argument_spec=RULES_ARGUMENT_SPEC,
        required_if=RULES_REQUIRED_IF,
        supports_check_mode=True)

    pfrule = PFSenseRuleModule(module)
    pfrule.run(module.params)
    pfrule.commit_changes()


if __name__ == '__main__':
    main()

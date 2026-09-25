from dataclasses import dataclass
from typing import List

@dataclass
class Finding:
    rule_id: str
    severity: str
    message: str
    remediation: str


def evaluate_spatial_api(max_features=None, pagination=False, auth_required=True, rate_limit=True) -> List[Finding]:
    findings=[]
    if max_features is None:
        findings.append(Finding("AP-API-001","HIGH","No explicit server-side feature limit.","Add bounded limits and pagination."))
    if not pagination:
        findings.append(Finding("AP-API-003","MEDIUM","No pagination contract is declared.","Add deterministic pagination for collection responses."))
    if not auth_required:
        findings.append(Finding("AP-SEC-001","HIGH","Endpoint has no declared authorization requirement.","Define and enforce access control appropriate to the data."))
    if not rate_limit:
        findings.append(Finding("AP-SEC-002","MEDIUM","No rate/resource protection is declared.","Add rate limiting or equivalent workload protection."))
    return findings


def evaluate_security_headers(cors_wildcard=False, browser_secret=False) -> List[Finding]:
    findings=[]
    if cors_wildcard:
        findings.append(Finding("AP-SEC-003","MEDIUM","Wildcard CORS may expose unintended browser access.","Restrict origins to the required trust boundary."))
    if browser_secret:
        findings.append(Finding("AP-SEC-004","HIGH","A provider secret is exposed to the browser.","Move the secret server-side or use a provider-approved restricted browser credential."))
    return findings

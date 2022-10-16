# ShadowFax

The aim of this Pentest is to assess the security of a clients endpoint ShadowFax. This report contains technical terms, but has been written so a non-technical reader with basic computing knowledge would understand it. Technical context will be provided in the appendices and screenshots. Should the reader encounter difficulties understanding any section of the report, reading the "Executive Summary" and the "Conclusions and Recommendations" section. For further help, contact the help department.&#x20;

### Some Definitions

**Hacker**: term given by the public that the cyber security industry more accurately call and attacker or intruder.

**Vulnerability:** Typically a bug or a misconfiguration in a computer program, or computer that can be abused to gain access on a computer

**Exploit:** A program or strategy to exploit a vulnerability.&#x20;

**Privilege Escalation:** A technique to escalate privileges on a computer, often to an admin user.

**Metasploit/Meterpreter:** A tool that was designed to execute various vulnerabilities automatically. Helpful for Penetration Testing

{% embed url="https://pentestreports.com/reports/BitesPenTesting/penetration-test-report.html" %}

## Hostname

| IP Addresses | Network                                |
| ------------ | -------------------------------------- |
| 10.0.6.52    | shadowfax.shire.org (different subnet) |
| 10.0.5.250   | fw-rivendell.shire.org                 |

### Target Overview

### Vulnerabilities&#x20;

#### Severity (9.8 Remote Code Execution) - AnyDesk CVE: [2020-13160](https://nvd.nist.gov/vuln/detail/CVE-2020-13160)

* > This vulnerability allows for remote commands to be executed. /etc/passwd can be viewed as well as other commands can be run. This exploit allows for a reverse shell to be established.
*   Mitigation

    > Update software

{% embed url="https://www.exploit-db.com/exploits/49613" %}

#### Severity (00 PwnKit) - PwnKit CVE:&#x20;

* > This vulnerability allows for remote commands to be executed. /etc/passwd can be viewed as well as other commands can be run. This exploit allows for a reverse shell to be established.
*   Mitigation

    > Update software

## Supporting Evidence

### Prerequisites



### Scanning and Enumeration

This is the live webpage active on the target. To enumerate further I inspected the webpage code using the network page and raw inspector. This showed me that there is a function being passed when the log files view file button is pressed. This can be seen in a screenshot below.

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption><p>Nmap scan of target</p></figcaption></figure>

#### SSL Certificate

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

### Foothold

#### Vulnerability Research



**MsVenom Payload Creation**

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

#### AnyDesk RCE Vulnerability

<figure><img src="../.gitbook/assets/image (1) (1) (3).png" alt=""><figcaption><p>Screenshot of custom edited payload</p></figcaption></figure>

#### Setting up Socat

{% embed url="https://technotes.noahbeckman.com/v/sec480-pentest-2/useful-things/socat" %}

#### Gaining a reverse shell

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption><p>reverse shell</p></figcaption></figure>

#### Upgrading shell



{% embed url="https://technotes.noahbeckman.com/v/sec480-pentest-2/useful-things/metasploit-shells" %}

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption><p>user flag</p></figcaption></figure>

### Privilege Escalation

Privilege escalation typically starts out with searching through currently running services, SUID bits, and more. The program Linpeas.sh is typically another good start that automatically runs through most of the checks. Often times this gives us the best place to look not an actual vulnerability.&#x20;

#### Enumeration

Linpeas

<figure><img src="../.gitbook/assets/image (3) (3).png" alt=""><figcaption><p>PwnKit CVE</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (48).png" alt=""><figcaption><p>running the exploit</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (49).png" alt=""><figcaption><p>root flag</p></figcaption></figure>

#### Persistence

<figure><img src="../.gitbook/assets/image (19).png" alt=""><figcaption><p>User creation</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption><p>SSHed into my account and in sudo group</p></figcaption></figure>

**Post Exploitation (Loot)**

{% embed url="https://app.gitbook.com/s/ARbxojkXZUSOB608QVbo/tools-and-loot/loot" %}
Loot Page
{% endembed %}

### Conclusions and Recommendations

In conclusion

### **Lab Issues**

****
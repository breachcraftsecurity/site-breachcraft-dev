# Stormspotter

**Type:** Python/React Application
**Purpose:** Azure Red Team tool for graphing Azure resources
**Platform:** Linux, macOS, Windows (Docker)
**Tags:** #azure #graph-database #enumeration #visualization #red-team

---

## Purpose

StormSpotter creates visual graphs of Azure environments:
- Resource relationships
- Permission mappings
- Attack path visualization
- Similar to BloodHound for Azure

---

## Installation

```bash
# Docker-based installation
git clone https://github.com/Azure/Stormspotter.git
cd Stormspotter
docker-compose up
```

---

## Data Collection

```bash
# Collect Azure data
cd stormcollector
python3 stormspotter.py -cli

# Authenticate to Azure
# Data collected to JSON files
```

---

## Visualization

```bash
# Access web interface
# http://localhost:9091

# Upload collected JSON files
# Explore graph visualization
```

---

## Pro Tips

💡 **Azure BloodHound**: Similar concept to BloodHound for Azure
💡 **Visual Analysis**: Interactive graph exploration
💡 **Docker-Based**: Easy deployment via containers
💡 **Red Team**: Identifies attack paths in Azure

---

## Resources

- GitHub: https://github.com/Azure/Stormspotter
- Company: Microsoft Azure (Red Team)

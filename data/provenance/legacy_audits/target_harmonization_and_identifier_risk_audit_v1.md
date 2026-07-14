# Target harmonization and identifier risk audit v1

The target universe is consistently 2,309 across D1, C3, D7, and D12. The D12 summary specifies HGNC canonical symbols with frozen UniProt cross-checks, four previous-symbol mappings, two aliases, removal of 36 alias-induced duplicate pairs, exclusion of eight composite strings and six nonhuman targets, and quarantine of two unresolved rows. No cross-stage target-count inconsistency was detected.

Current risk is **MAJOR transparency risk, LOW demonstrated leakage risk**. Main-text explanation is substantially adequate but does not replace a row-level, licence-compliant mapping appendix. Add source string, source namespace, species, canonical symbol/ID, mapping type, evidence/snapshot version, disposition, duplicate group, and rule version. State how obsolete IDs, aliases, composites, and species ambiguity are handled. If full rows cannot be redistributed, publish schemas, counts, hashes, pseudocode, and a controlled audit route.

No experiment redo is required because the mapping was frozen and counts are internally consistent. Redo would be considered only if a future controlled audit reveals target-universe drift or materially incorrect mappings that changed formal inputs.

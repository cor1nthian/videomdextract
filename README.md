# videomdextract
Media file metadata extractor.Extracted info resides in script folder (bt default).

Script uses fffmpeg exe tool, read more on this in script comments

Tested with Windows 10

Can be called with arguments:
| Ppsition | Suggested type | Description |
| --- | --- | --- |
| 1 | String | Path to mediafile |

Script return codes:
| Code | Description |
| --- | --- |
| 1 | FFmpeg exe does not exist |
| 2 | Media file path nor set |
| 3 | Media file path does not exist |

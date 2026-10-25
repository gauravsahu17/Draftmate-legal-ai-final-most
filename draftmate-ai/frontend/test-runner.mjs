import {mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
const temp=resolve('.test-temp');mkdirSync(temp,{recursive:true});
execFileSync(process.execPath,['node_modules/vitest/vitest.mjs','run'],{stdio:'inherit',env:{...process.env,TEMP:temp,TMP:temp,TMPDIR:temp}});

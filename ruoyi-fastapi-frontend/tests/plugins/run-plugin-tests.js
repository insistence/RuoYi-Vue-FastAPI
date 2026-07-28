const { readdirSync } = require('fs')
const { join, relative } = require('path')

const collectTestFiles = root => {
  const entries = readdirSync(root, { withFileTypes: true })
  const testFiles = []

  for (const entry of entries) {
    const entryPath = join(root, entry.name)
    if (entry.isDirectory()) {
      testFiles.push(...collectTestFiles(entryPath))
      continue
    }
    if (entry.isFile() && entry.name.endsWith('.test.js')) {
      testFiles.push(entryPath)
    }
  }

  return testFiles.sort()
}

const testFiles = collectTestFiles(__dirname)

if (testFiles.length === 0) {
  console.error('No plugin tests found')
  process.exitCode = 1
} else {
  let failedCount = 0

  for (const testFile of testFiles) {
    const testName = relative(__dirname, testFile)

    try {
      require(testFile)
      console.log(`ok ${testName}`)
    } catch (error) {
      failedCount += 1
      console.error(`not ok ${testName}`)
      console.error(error && error.stack ? error.stack : error)
    }
  }

  if (failedCount > 0) {
    console.error(`Plugin tests failed: ${failedCount}/${testFiles.length}`)
    process.exitCode = 1
  } else {
    console.log(`Plugin tests passed: ${testFiles.length}`)
  }
}

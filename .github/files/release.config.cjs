module.exports = {
    branches: ['main'],
    tagFormat: '${version}',
    plugins: [
        [
            '@semantic-release/commit-analyzer',
            {
                preset: 'angular',
                parserOpts: {
                    noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING'],
                },
            },
        ],
        [
            '@semantic-release/release-notes-generator',
            {
                preset: 'angular',
                parserOpts: {
                    noteKeywords: ['BREAKING CHANGE', 'BREAKING CHANGES', 'BREAKING'],
                },
                writerOpts: {
                    commitsSort: ['subject', 'scope'],
                },
            },
        ],
        [
            '@semantic-release/changelog',
            {
                changelogFile: 'CHANGELOG.md',
            },
        ],
        [
            '@semantic-release/exec',
            {
                prepareCmd: [
                    "sed -i 's/^version:.*/version: ${nextRelease.version}/g' galaxy.yml",
                    "sed -i 's/^export NEBULA_VERSION=.*/export NEBULA_VERSION=${nextRelease.version}/g' README.md",
                    "poetry version ${nextRelease.version} && ansible-galaxy collection build",
                ].join(' && '),
                // successCmd:
                //     'ansible-galaxy collection publish arpanrec-nebula-${nextRelease.version}.tar.gz --api-key ${process.env.GALAXY_API_KEY}',
            },
        ],
        [
            '@semantic-release/git',
            {
                assets: ['galaxy.yml', 'CHANGELOG.md', 'pyproject.toml', 'README.md'],
                message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
            },
        ],
    ],
};

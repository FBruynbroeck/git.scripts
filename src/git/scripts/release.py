# encoding: utf-8
"""
release.py

Created by FBruynbroeck on 2015-09-29.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""
import os
import logging

from zest.releaser import baserelease
from zest.releaser import utils
logger = logging.getLogger(__name__)
BUILDOUT = os.environ.get('BUILDOUT')
BUILDOUTHISTORYFILE = "%s/CHANGES.txt" % BUILDOUT


def getHistoryLines(vcs):
    history = vcs.history_file()
    if not history:
        return None, None
    history_lines, history_encoding = utils.read_text_file(history)
    history_lines = history_lines.split('\n')
    return history_lines, history_encoding


def getCurrentChangeLogs(history_lines, headings):
    i = 0
    for heading in headings:
        i += 1
        if heading['date'] != 'unreleased':
            first = heading
            break
    if len(headings) == i:
        logger.warn("No release version")
        return
    second = headings[i]
    changelogs = history_lines[first['line']+2:second['line']-2]
    version = first['version']
    return changelogs, version


def getBuildoutHistoryLines():
    history_lines, history_encoding = utils.read_text_file(BUILDOUTHISTORYFILE)
    history_lines = history_lines.split('\n')
    return history_lines, history_encoding


def updateBuildoutChangeLogs(history_lines, history_encoding, headings, changelogs, package, version):
    inject_location = headings[0]['line']
    inject = ['', '- %s %s' % (package, version)]
    indentchangelogs = []
    for changelog in changelogs:
        if changelog:
            changelog = '  %s' % changelog
        indentchangelogs.append(changelog)
    inject.extend(indentchangelogs)
    history_lines[inject_location+2:inject_location+2] = inject
    contents = u'\n'.join(history_lines)
    utils.write_text_file(BUILDOUTHISTORYFILE, contents, history_encoding)


def upgradeBuildoutVersion(package, version):
    # Read in the file
    filedata = None
    filename = '%s/versions_prod.cfg' % BUILDOUT
    with open(filename, 'r') as file:
        filedata = file.read()
    filedata = filedata.split('\n')
    result = []
    match = False
    newversion = '%s = %s' % (package, version)
    for line in filedata:
        if package in line:
            line = newversion
            match = True
        result.append(line)
    if not match:
        result.pop()
        result.append(newversion)
    result = u'\n'.join(result)

    # Write the file out again
    with open(filename, 'w') as file:
        file.write(result)


def extractHeadings(history_lines):
    if not history_lines:
        logger.warn("No history file found")
        return
    headings = utils.extract_headings_from_history(history_lines)
    if not len(headings):
        logger.warn("No detectable existing version headings in the "
                    "history file.")
        return
    return headings


def change_log():
    utils.parse_options()
    utils.configure_logging()
    logger.info('Starting changelogrelease.')
    if not utils.ask("OK to update ChangeLog"):
        return
    if not BUILDOUT:
        logger.warn("No BUILDOUT environment variable")
        return
    vcs = baserelease.Basereleaser().vcs
    package = vcs.name
    buildoutpackage = os.path.split(os.path.abspath(BUILDOUT))[1]
    if package == buildoutpackage:
        logger.warn("It's the buildout")
        return

    # Current buildout
    history_lines, history_encoding = getHistoryLines(vcs)
    headings = extractHeadings(history_lines)
    if not headings:
        return
    changelogs, version = getCurrentChangeLogs(history_lines, headings)

    # Master Buildout
    history_lines, history_encoding = getBuildoutHistoryLines()
    headings = extractHeadings(history_lines)
    if not headings:
        return
    updateBuildoutChangeLogs(history_lines, history_encoding, headings, changelogs, package, version)
    upgradeBuildoutVersion(package, version)
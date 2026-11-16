#!/usr/bin/env python3
"""Build the Melinoe Moss dark and light themes from one palette.

Run: python3 scripts/build-moss.py
The script writes themes/moss-dark-color-theme.json and
themes/moss-light-color-theme.json, then prints a WCAG contrast report.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Palette sources: moss and forest teal, meadow grass, sunflower yellow,
# summer sky blue, quilt terracotta, cherry berry, and bellflower lavender.
PALETTES = {
    "dark": {
        # Main palette: sage #62ab71, moss #327b4f, forest #246143.
        "name": "Melinoe Moss Dark",
        "kind": "dark",
        "bg": "#163626",
        "bgDeep": "#112d1f",
        "bgRaised": "#1c412e",
        "bgHover": "#246143",
        "lineHl": "#1b3e2c",
        "border": "#245039",
        "terminalBg": "#112d1f",
        "fg": "#e1eadb",
        "fgMuted": "#a9c2ae",
        "fgFaint": "#5f8a6c",
        "comment": "#8fb299",
        "accent": "#62ab71",
        "accentFg": "#0e2619",
        "accentHover": "#76bd84",
        "selection": "#327b4f99",
        "selectionInactive": "#327b4f55",
        "wordHl": "#8fc8e033",
        "findMatch": "#e6c97a55",
        "findMatchHl": "#e6c97a2a",
        "keyword": "#8fd19c",
        "string": "#e6c97a",
        "function": "#8fc8e0",
        "type": "#7fd3c0",
        "number": "#eaaa7f",
        "tag": "#eca4ae",
        "lavender": "#c3b2e4",
        "property": "#cfdfc6",
        "punct": "#a9c2ae",
        "error": "#f08f85",
        "warning": "#e6c97a",
        "info": "#8fc8e0",
        "added": "#76bd84",
        "modified": "#8fc8e0",
        "deleted": "#f08f85",
        "ansi": {
            "Black": "#245039", "Red": "#f08f85", "Green": "#62ab71",
            "Yellow": "#e6c97a", "Blue": "#8fc8e0", "Magenta": "#c3b2e4",
            "Cyan": "#7fd3c0", "White": "#e1eadb",
            "BrightBlack": "#6f9a7c", "BrightRed": "#f5a89f",
            "BrightGreen": "#8fd19c", "BrightYellow": "#f0d896",
            "BrightBlue": "#abd7ea", "BrightMagenta": "#d4c7ec",
            "BrightCyan": "#9be0cf", "BrightWhite": "#f2f6ee",
        },
    },
    "light": {
        "name": "Melinoe Moss Light",
        "kind": "light",
        "bg": "#f5f2e6",
        "bgDeep": "#ece8d8",
        "terminalBg": "#e2dcc6",
        "bgRaised": "#fbf9f1",
        "bgHover": "#e3dfcb",
        "lineHl": "#eeeadb",
        "border": "#dcd6c1",
        "fg": "#2f3a2c",
        "fgMuted": "#5d6656",
        "fgFaint": "#979c86",
        "comment": "#646c59",
        "accent": "#4d7d2c",
        "accentFg": "#fbf9f1",
        "accentHover": "#5c8e38",
        "selection": "#8fbf6a55",
        "selectionInactive": "#8fbf6a30",
        "wordHl": "#2c658922",
        "findMatch": "#e0b84a70",
        "findMatchHl": "#e0b84a38",
        "keyword": "#437321",
        "string": "#86620f",
        "function": "#2c6589",
        "type": "#1c7262",
        "number": "#a5522a",
        "tag": "#a83b58",
        "lavender": "#6a52a3",
        "property": "#3f4c3a",
        "punct": "#5f6a58",
        "error": "#b8402f",
        "warning": "#8a5f08",
        "info": "#2c6589",
        "added": "#4d8a2c",
        "modified": "#2c6589",
        "deleted": "#b8402f",
        "ansi": {
            "Black": "#2f3a2c", "Red": "#b8402f", "Green": "#437321",
            "Yellow": "#86620f", "Blue": "#2c6589", "Magenta": "#6a52a3",
            "Cyan": "#1c7262", "White": "#d8d3bf",
            "BrightBlack": "#6c7461", "BrightRed": "#cc5a48",
            "BrightGreen": "#55882f", "BrightYellow": "#a07a1c",
            "BrightBlue": "#3f7aa0", "BrightMagenta": "#7f68b8",
            "BrightCyan": "#2d8775", "BrightWhite": "#fbf9f1",
        },
    },
}


def workbench(p):
    c = {
        # Base
        "foreground": p["fg"],
        "descriptionForeground": p["fgMuted"],
        "disabledForeground": p["fgFaint"],
        "errorForeground": p["error"],
        "focusBorder": p["accent"] + "99",
        "selection.background": p["selection"],
        "widget.shadow": "#00000033" if p["kind"] == "dark" else "#4a503c22",
        "icon.foreground": p["fgMuted"],
        "textLink.foreground": p["function"],
        "textLink.activeForeground": p["accent"],
        "textCodeBlock.background": p["bgDeep"],
        "textBlockQuote.background": p["bgDeep"],
        "textBlockQuote.border": p["accent"],
        "textPreformat.foreground": p["string"],
        "sash.hoverBorder": p["accent"],

        # Title bar, activity bar, side bar
        "titleBar.activeBackground": p["bgDeep"],
        "titleBar.activeForeground": p["fgMuted"],
        "titleBar.inactiveBackground": p["bgDeep"],
        "titleBar.inactiveForeground": p["fgFaint"],
        "titleBar.border": p["border"],
        "activityBar.background": p["bgDeep"],
        "activityBar.foreground": p["accent"],
        "activityBar.inactiveForeground": p["fgFaint"],
        "activityBar.activeBorder": p["accent"],
        "activityBar.border": p["border"],
        "activityBarBadge.background": p["accent"],
        "activityBarBadge.foreground": p["accentFg"],
        "sideBar.background": p["bgDeep"],
        "sideBar.foreground": p["fgMuted"],
        "sideBar.border": p["border"],
        "sideBarTitle.foreground": p["fg"],
        "sideBarSectionHeader.background": p["bgDeep"],
        "sideBarSectionHeader.foreground": p["fg"],
        "sideBarSectionHeader.border": p["border"],

        # Lists and trees
        "list.activeSelectionBackground": p["bgHover"],
        "list.activeSelectionForeground": p["fg"],
        "list.inactiveSelectionBackground": p["bgHover"],
        "list.inactiveSelectionForeground": p["fg"],
        "list.hoverBackground": p["lineHl"] if p["kind"] == "dark" else p["bgHover"] + "99",
        "list.hoverForeground": p["fg"],
        "list.focusBackground": p["bgHover"],
        "list.focusForeground": p["fg"],
        "list.focusOutline": p["accent"] + "66",
        "list.highlightForeground": p["accent"],
        "list.dropBackground": p["selection"],
        "list.errorForeground": p["error"],
        "list.warningForeground": p["warning"],
        "tree.indentGuidesStroke": p["border"],
        "listFilterWidget.background": p["bgRaised"],
        "listFilterWidget.outline": p["accent"],
        "listFilterWidget.noMatchesOutline": p["error"],

        # Editor groups and tabs
        "editorGroup.border": p["border"],
        "editorGroup.emptyBackground": p["bg"],
        "editorGroupHeader.tabsBackground": p["bgDeep"],
        "editorGroupHeader.tabsBorder": p["border"],
        "tab.activeBackground": p["bg"],
        "tab.activeForeground": p["fg"],
        "tab.activeBorderTop": p["accent"],
        "tab.inactiveBackground": p["bgDeep"],
        "tab.inactiveForeground": p["fgMuted"],
        "tab.hoverBackground": p["lineHl"],
        "tab.border": p["border"],
        "tab.unfocusedActiveForeground": p["fgMuted"],
        "breadcrumb.background": p["bg"],
        "breadcrumb.foreground": p["fgMuted"],
        "breadcrumb.focusForeground": p["fg"],
        "breadcrumb.activeSelectionForeground": p["accent"],

        # Editor
        "editor.background": p["bg"],
        "editor.foreground": p["fg"],
        "editorLineNumber.foreground": p["fgFaint"],
        "editorLineNumber.activeForeground": p["fgMuted"],
        "editorCursor.foreground": p["accent"],
        "editor.selectionBackground": p["selection"],
        "editor.inactiveSelectionBackground": p["selectionInactive"],
        "editor.selectionHighlightBackground": p["selectionInactive"],
        "editor.wordHighlightBackground": p["wordHl"],
        "editor.wordHighlightStrongBackground": p["wordHl"],
        "editor.findMatchBackground": p["findMatch"],
        "editor.findMatchHighlightBackground": p["findMatchHl"],
        "editor.findRangeHighlightBackground": p["selectionInactive"],
        "editor.rangeHighlightBackground": p["selectionInactive"],
        "editor.hoverHighlightBackground": p["wordHl"],
        "editor.lineHighlightBackground": p["lineHl"],
        "editor.lineHighlightBorder": p["lineHl"],
        "editorWhitespace.foreground": p["border"],
        "editorIndentGuide.background1": p["border"],
        "editorIndentGuide.activeBackground1": p["fgFaint"],
        "editorRuler.foreground": p["border"],
        "editorBracketMatch.background": p["accent"] + "22",
        "editorBracketMatch.border": p["accent"] + "88",
        "editorBracketHighlight.foreground1": p["string"],
        "editorBracketHighlight.foreground2": p["lavender"],
        "editorBracketHighlight.foreground3": p["function"],
        "editorBracketHighlight.foreground4": p["number"],
        "editorBracketHighlight.foreground5": p["type"],
        "editorBracketHighlight.foreground6": p["tag"],
        "editorBracketHighlight.unexpectedBracket.foreground": p["error"],
        "editor.foldBackground": p["selectionInactive"],
        "editorLink.activeForeground": p["function"],
        "editorCodeLens.foreground": p["fgFaint"],
        "editorInlayHint.foreground": p["fgMuted"],
        "editorInlayHint.background": p["bgRaised"],
        "editorGhostText.foreground": p["fgFaint"],
        "editorError.foreground": p["error"],
        "editorWarning.foreground": p["warning"],
        "editorInfo.foreground": p["info"],
        "editorHint.foreground": p["accent"],
        "editorGutter.background": p["bg"],
        "editorGutter.addedBackground": p["added"],
        "editorGutter.modifiedBackground": p["modified"],
        "editorGutter.deletedBackground": p["deleted"],
        "editorGutter.foldingControlForeground": p["fgMuted"],
        "editorOverviewRuler.border": p["border"],
        "editorOverviewRuler.errorForeground": p["error"],
        "editorOverviewRuler.warningForeground": p["warning"],
        "editorOverviewRuler.addedForeground": p["added"],
        "editorOverviewRuler.modifiedForeground": p["modified"],
        "editorOverviewRuler.deletedForeground": p["deleted"],
        "editorOverviewRuler.findMatchForeground": p["string"],
        "minimap.background": p["bg"],
        "minimap.findMatchHighlight": p["string"],
        "minimap.selectionHighlight": p["accent"],
        "minimap.errorHighlight": p["error"],
        "minimap.warningHighlight": p["warning"],
        "minimapGutter.addedBackground": p["added"],
        "minimapGutter.modifiedBackground": p["modified"],
        "minimapGutter.deletedBackground": p["deleted"],

        # Widgets
        "editorWidget.background": p["bgRaised"],
        "editorWidget.foreground": p["fg"],
        "editorWidget.border": p["border"],
        "editorSuggestWidget.background": p["bgRaised"],
        "editorSuggestWidget.border": p["border"],
        "editorSuggestWidget.foreground": p["fg"],
        "editorSuggestWidget.highlightForeground": p["accent"],
        "editorSuggestWidget.focusHighlightForeground": p["accent"],
        "editorSuggestWidget.selectedBackground": p["bgHover"],
        "editorSuggestWidget.selectedForeground": p["fg"],
        "editorHoverWidget.background": p["bgRaised"],
        "editorHoverWidget.foreground": p["fg"],
        "editorHoverWidget.border": p["border"],
        "quickInput.background": p["bgRaised"],
        "quickInput.foreground": p["fg"],
        "quickInputList.focusBackground": p["bgHover"],
        "quickInputList.focusForeground": p["fg"],
        "pickerGroup.border": p["border"],
        "pickerGroup.foreground": p["accent"],
        "peekView.border": p["accent"],
        "peekViewEditor.background": p["bgDeep"],
        "peekViewEditorGutter.background": p["bgDeep"],
        "peekViewEditor.matchHighlightBackground": p["findMatch"],
        "peekViewResult.background": p["bgRaised"],
        "peekViewResult.fileForeground": p["fg"],
        "peekViewResult.lineForeground": p["fgMuted"],
        "peekViewResult.matchHighlightBackground": p["findMatch"],
        "peekViewResult.selectionBackground": p["bgHover"],
        "peekViewResult.selectionForeground": p["fg"],
        "peekViewTitle.background": p["bgRaised"],
        "peekViewTitleLabel.foreground": p["fg"],
        "peekViewTitleDescription.foreground": p["fgMuted"],

        # Inputs and controls
        # Search fields (Extensions, Settings, Find) use these keys.
        # Keep the dark input dark, with a visible border and a readable placeholder.
        "input.background": p["bgRaised"] if p["kind"] == "dark" else "#ffffff",
        "input.foreground": p["fg"],
        "input.border": p["fgFaint"] if p["kind"] == "dark" else p["border"],
        "input.placeholderForeground": p["fgMuted"],
        "settings.textInputBackground": p["bgRaised"] if p["kind"] == "dark" else "#ffffff",
        "settings.textInputForeground": p["fg"],
        "settings.textInputBorder": p["fgFaint"] if p["kind"] == "dark" else p["border"],
        "settings.numberInputBackground": p["bgRaised"] if p["kind"] == "dark" else "#ffffff",
        "settings.numberInputForeground": p["fg"],
        "settings.numberInputBorder": p["fgFaint"] if p["kind"] == "dark" else p["border"],
        "searchEditor.textInputBorder": p["fgFaint"] if p["kind"] == "dark" else p["border"],
        "inputOption.activeBackground": p["accent"] + "33",
        "inputOption.activeBorder": p["accent"],
        "inputOption.activeForeground": p["fg"],
        "inputValidation.errorBackground": p["bgRaised"],
        "inputValidation.errorBorder": p["error"],
        "inputValidation.warningBackground": p["bgRaised"],
        "inputValidation.warningBorder": p["warning"],
        "inputValidation.infoBackground": p["bgRaised"],
        "inputValidation.infoBorder": p["info"],
        "dropdown.background": p["bgRaised"],
        "dropdown.foreground": p["fg"],
        "dropdown.border": p["border"],
        "checkbox.background": p["bgRaised"],
        "checkbox.foreground": p["fg"],
        "checkbox.border": p["border"],
        "button.background": p["accent"],
        "button.foreground": p["accentFg"],
        "button.hoverBackground": p["accentHover"],
        "button.secondaryBackground": p["bgHover"],
        "button.secondaryForeground": p["fg"],
        "button.secondaryHoverBackground": p["border"],
        "badge.background": p["accent"],
        "badge.foreground": p["accentFg"],
        "progressBar.background": p["accent"],
        "scrollbar.shadow": "#00000022",
        "scrollbarSlider.background": p["fgFaint"] + "40",
        "scrollbarSlider.hoverBackground": p["fgFaint"] + "70",
        "scrollbarSlider.activeBackground": p["fgFaint"] + "99",
        "keybindingLabel.background": p["bgHover"],
        "keybindingLabel.foreground": p["fg"],
        "keybindingLabel.border": p["border"],
        "keybindingLabel.bottomBorder": p["border"],

        # Menus
        "menu.background": p["bgRaised"],
        "menu.foreground": p["fg"],
        "menu.selectionBackground": p["bgHover"],
        "menu.selectionForeground": p["fg"],
        "menu.separatorBackground": p["border"],
        "menu.border": p["border"],
        "menubar.selectionBackground": p["bgHover"],
        "menubar.selectionForeground": p["fg"],

        # Panel and terminal
        "panel.background": p["bgDeep"],
        "panel.border": p["border"],
        "panelTitle.activeBorder": p["accent"],
        "panelTitle.activeForeground": p["fg"],
        "panelTitle.inactiveForeground": p["fgMuted"],
        "panelSection.border": p["border"],
        "terminal.background": p["terminalBg"],
        "terminal.foreground": p["fg"],
        "terminal.selectionBackground": p["selection"],
        "terminalCursor.foreground": p["accent"],
        "terminal.border": p["border"],

        # Status bar
        "statusBar.background": p["bgDeep"],
        "statusBar.foreground": p["fgMuted"],
        "statusBar.border": p["border"],
        "statusBar.noFolderBackground": p["bgDeep"],
        "statusBar.noFolderForeground": p["fgMuted"],
        "statusBar.debuggingBackground": p["number"],
        "statusBar.debuggingForeground": p["accentFg"],
        "statusBarItem.hoverBackground": p["bgHover"],
        "statusBarItem.activeBackground": p["border"],
        "statusBarItem.remoteBackground": p["accent"],
        "statusBarItem.remoteForeground": p["accentFg"],
        "statusBarItem.errorBackground": p["error"],
        "statusBarItem.errorForeground": p["accentFg"],

        # Notifications
        "notifications.background": p["bgRaised"],
        "notifications.foreground": p["fg"],
        "notifications.border": p["border"],
        "notificationCenterHeader.background": p["bgDeep"],
        "notificationCenterHeader.foreground": p["fg"],
        "notificationToast.border": p["border"],
        "notificationsErrorIcon.foreground": p["error"],
        "notificationsWarningIcon.foreground": p["warning"],
        "notificationsInfoIcon.foreground": p["info"],

        # Git and diff
        "gitDecoration.addedResourceForeground": p["added"],
        "gitDecoration.untrackedResourceForeground": p["added"],
        "gitDecoration.modifiedResourceForeground": p["modified"],
        "gitDecoration.stageModifiedResourceForeground": p["modified"],
        "gitDecoration.deletedResourceForeground": p["deleted"],
        "gitDecoration.stageDeletedResourceForeground": p["deleted"],
        "gitDecoration.conflictingResourceForeground": p["number"],
        "gitDecoration.ignoredResourceForeground": p["fgFaint"],
        "gitDecoration.submoduleResourceForeground": p["lavender"],
        "diffEditor.insertedTextBackground": p["added"] + "22",
        "diffEditor.removedTextBackground": p["deleted"] + "22",
        "diffEditor.insertedLineBackground": p["added"] + "14",
        "diffEditor.removedLineBackground": p["deleted"] + "14",
        "merge.currentHeaderBackground": p["added"] + "55",
        "merge.currentContentBackground": p["added"] + "22",
        "merge.incomingHeaderBackground": p["function"] + "55",
        "merge.incomingContentBackground": p["function"] + "22",
        "merge.commonHeaderBackground": p["fgFaint"] + "55",
        "merge.commonContentBackground": p["fgFaint"] + "22",

        # Debug and settings
        "debugToolBar.background": p["bgRaised"],
        "debugExceptionWidget.background": p["bgRaised"],
        "debugExceptionWidget.border": p["error"],
        "settings.headerForeground": p["fg"],
        "settings.modifiedItemIndicator": p["accent"],
        "settings.focusedRowBackground": p["lineHl"],
        "walkThrough.embeddedEditorBackground": p["bgDeep"],
    }
    for k, v in p["ansi"].items():
        c["terminal.ansi" + k] = v
    return c


def token_colors(p):
    def rule(name, scope, fg, style=None):
        s = {"foreground": fg}
        if style is not None:
            s["fontStyle"] = style
        return {"name": name, "scope": scope, "settings": s}

    return [
        rule("Comments", ["comment", "punctuation.definition.comment", "string.comment"], p["comment"], "italic"),
        rule("Doc comment tags", ["comment keyword", "comment storage.type", "storage.type.class.jsdoc"], p["lavender"], "italic"),
        rule("Doc comment variables", ["comment variable", "comment entity.name.type"], p["type"], "italic"),
        rule("Variables", ["variable", "variable.other", "variable.other.readwrite", "entity.name.variable"], p["fg"]),
        rule("Parameters", ["variable.parameter", "meta.parameter variable"], p["number"], "italic"),
        rule("Properties", ["variable.other.property", "variable.other.object.property", "meta.object-literal.key", "support.variable.property", "entity.name.field"], p["property"]),
        rule("Language variables", ["variable.language", "variable.language.this", "variable.language.self", "variable.parameter.function.language.special.self"], p["lavender"], "italic"),
        rule("Keywords", ["keyword", "keyword.control", "storage", "storage.type", "storage.modifier", "keyword.operator.new", "keyword.operator.expression", "keyword.operator.logical.python"], p["keyword"]),
        rule("Operators", ["keyword.operator", "punctuation.accessor", "punctuation.separator.key-value"], p["punct"]),
        rule("Punctuation", ["punctuation", "meta.brace", "punctuation.terminator", "punctuation.separator"], p["punct"]),
        rule("Strings", ["string", "string.quoted", "string.template", "punctuation.definition.string"], p["string"]),
        rule("Template expressions", ["punctuation.definition.template-expression", "punctuation.section.embedded"], p["keyword"]),
        rule("Escapes and regex", ["constant.character.escape", "string.regexp", "constant.other.character-class.regexp", "keyword.operator.quantifier.regexp"], p["tag"]),
        rule("Numbers and constants", ["constant.numeric", "constant.language", "constant.other", "support.constant", "variable.other.constant", "variable.other.enummember", "constant.character"], p["number"]),
        rule("Functions", ["entity.name.function", "support.function", "meta.function-call entity.name.function", "variable.function", "meta.require", "keyword.other.special-method"], p["function"]),
        rule("Types and classes", ["entity.name.type", "entity.name.class", "support.type", "support.class", "entity.other.inherited-class", "entity.name.namespace", "storage.type.primitive", "storage.type.built-in", "entity.name.type.module"], p["type"]),
        rule("Decorators and annotations", ["meta.decorator", "punctuation.decorator", "storage.type.annotation", "entity.name.function.decorator", "meta.attribute"], p["lavender"]),
        rule("Tags", ["entity.name.tag", "meta.tag.sgml", "punctuation.definition.tag"], p["keyword"]),
        rule("Tag brackets", ["punctuation.definition.tag.begin", "punctuation.definition.tag.end"], p["punct"]),
        rule("Components", ["support.class.component", "entity.name.tag.tsx", "entity.name.tag.jsx"], p["type"]),
        rule("Attributes", ["entity.other.attribute-name"], p["number"], "italic"),
        rule("CSS selectors", ["entity.other.attribute-name.class.css", "entity.other.attribute-name.id.css", "entity.other.attribute-name.pseudo-class", "entity.other.attribute-name.pseudo-element"], p["function"]),
        rule("CSS properties", ["support.type.property-name", "support.type.vendored.property-name"], p["property"]),
        rule("CSS values", ["support.constant.property-value", "support.constant.color", "keyword.other.unit"], p["number"]),
        rule("JSON keys", ["support.type.property-name.json", "support.type.property-name.json punctuation"], p["function"]),
        rule("YAML and TOML keys", ["entity.name.tag.yaml", "support.type.property-name.toml", "keyword.key.toml"], p["function"]),
        rule("Markdown headings", ["markup.heading", "markup.heading entity.name", "entity.name.section.markdown", "punctuation.definition.heading.markdown"], p["keyword"], "bold"),
        rule("Markdown bold", ["markup.bold", "punctuation.definition.bold"], p["number"], "bold"),
        rule("Markdown italic", ["markup.italic", "punctuation.definition.italic"], p["lavender"], "italic"),
        rule("Markdown strikethrough", ["markup.strikethrough"], p["comment"], "strikethrough"),
        rule("Markdown code", ["markup.inline.raw", "markup.fenced_code.block", "markup.raw"], p["string"]),
        rule("Markdown links", ["markup.underline.link", "string.other.link"], p["function"]),
        rule("Markdown lists and quotes", ["punctuation.definition.list.begin.markdown", "markup.quote", "punctuation.definition.quote"], p["tag"]),
        rule("Diff inserted", ["markup.inserted", "meta.diff.header.to-file"], p["added"]),
        rule("Diff deleted", ["markup.deleted", "meta.diff.header.from-file"], p["deleted"]),
        rule("Diff changed", ["markup.changed", "meta.diff.range"], p["modified"]),
        rule("Invalid", ["invalid", "invalid.illegal"], p["error"]),
        rule("Deprecated", ["invalid.deprecated"], p["warning"], "strikethrough"),
    ]


def semantic_tokens(p):
    return {
        "variable": p["fg"],
        "variable.readonly": p["number"],
        "variable.defaultLibrary": p["type"],
        "parameter": {"foreground": p["number"], "italic": True},
        "property": p["property"],
        "property.readonly": p["property"],
        "function": p["function"],
        "method": p["function"],
        "class": p["type"],
        "interface": p["type"],
        "enum": p["type"],
        "enumMember": p["number"],
        "type": p["type"],
        "typeParameter": {"foreground": p["type"], "italic": True},
        "namespace": p["type"],
        "decorator": p["lavender"],
        "macro": p["lavender"],
        "selfKeyword": {"foreground": p["lavender"], "italic": True},
        "keyword": p["keyword"],
        "string": p["string"],
        "number": p["number"],
        "*.deprecated": {"strikethrough": True},
    }


# WCAG 2 contrast check -------------------------------------------------------

def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    h = hex_color.lstrip("#")[:6]
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def report(key, p):
    checks = [
        ("fg", "bg", 7.0), ("fg", "bgDeep", 7.0), ("fgMuted", "bgDeep", 4.5),
        ("comment", "bg", 4.5), ("fgFaint", "bg", 2.0),
        ("accentFg", "accent", 4.5),
    ]
    checks += [(t, "bg", 4.5) for t in (
        "keyword", "string", "function", "type", "number", "tag",
        "lavender", "property", "punct", "error", "warning")]
    print(f"\n{p['name']}")
    bad = 0
    for fg, bg, minimum in checks:
        ratio = contrast(p[fg], p[bg])
        flag = "ok " if ratio >= minimum else "LOW"
        bad += ratio < minimum
        print(f"  {flag} {fg:>9} on {bg:<7} {ratio:5.2f}  (min {minimum})")
    return bad


def main():
    bad = 0
    for key, p in PALETTES.items():
        theme = {
            "$schema": "vscode://schemas/color-theme",
            "name": p["name"],
            "type": p["kind"],
            "semanticHighlighting": True,
            "colors": workbench(p),
            "tokenColors": token_colors(p),
            "semanticTokenColors": semantic_tokens(p),
        }
        out = ROOT / "themes" / f"moss-{key}-color-theme.json"
        out.write_text(json.dumps(theme, indent=2) + "\n")
        print(f"wrote {out.relative_to(ROOT)}")
        bad += report(key, p)
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()

# CloudPedagogy Word-to-Reveal.js Renderer

Convert structured Microsoft Word documents into Quarto Reveal.js presentations.

The renderer allows authors to prepare presentation content in Word using familiar heading styles, paragraphs, lists, tables and images. It converts each document into a Quarto Markdown (`.qmd`) presentation, extracts embedded media, produces a QA report and can optionally render the presentation to standalone HTML with Quarto.

> **Quarto is required for the finished presentation**
>
> The Python converter can run without Quarto, but it will produce only the
> intermediate `.qmd` source file, extracted media and QA report. Quarto must
> be installed to render these files as a complete interactive Reveal.js HTML
> presentation.
>
> - Run without `--render` to generate the `.qmd`, media and QA report.
> - Run with `--render` to generate the finished HTML presentation.

## Live demo

[Open the Vaccine Effectiveness presentation](http://cloudpedagogy-word-revealjs-renderer.s3-website.eu-west-2.amazonaws.com/Vaccine_Effectiveness_Slide_Test_slides.html#/title-slide)

## Features

- converts `.docx` files into Quarto Reveal.js presentations;
- uses Word Heading styles to define the presentation and slides;
- preserves paragraphs, bullet lists, tables and inline images;
- extracts embedded images into a local media folder;
- supports YouTube, Panopto and generic iframe embeds;
- supports configurable Reveal.js themes;
- processes one or many Word documents using a glob pattern;
- generates a QA report for every presentation;
- identifies images with missing alternative text;
- uses Quarto to render the generated `.qmd` file as a complete Reveal.js HTML presentation.

## Project files

```text
.
├── README.md
├── requirements.txt
├── word_to_revealjs.py
├── Vaccine_Effectiveness_Slide_Test.docx
├── imports/
│   └── presentations/
└── output/
    └── presentations/
```

## Requirements

- Python 3.10 or later
- [Quarto](https://quarto.org/docs/get-started/) for HTML rendering
- Python packages:
  - [Mammoth](https://github.com/mwilliamson/python-mammoth)
  - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

The Python converter can generate the `.qmd` source, extracted media and QA report without Quarto. This is an intermediate output rather than the finished presentation. Quarto is required when using `--render` or when rendering the generated presentation manually.

## Installation

Download or clone the repository, then open Terminal in the repository root.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Confirm that Quarto is available:

```bash
quarto --version
```

If the command is not found, install Quarto from the [official Quarto website](https://quarto.org/docs/get-started/).

## Word authoring structure

The default conversion rules are:

| Word content | Output |
|---|---|
| First Heading 1 | Presentation title |
| Heading 2 | New slide |
| Normal paragraphs | Slide text |
| Word bullet or numbered lists | Slide lists |
| Word tables | HTML tables |
| Inline images | Extracted presentation images |

Use Word's built-in styles rather than only changing the visual appearance of the text.

### Example structure

```text
Introduction to Vaccine Effectiveness       [Heading 1]

What is Vaccine Effectiveness?              [Heading 2]

Measures how well a vaccine performs        [List Bullet]
Different from efficacy measured in trials  [List Bullet]

Why Does It Matter?                         [Heading 2]

Supports vaccination policy.                [Normal]
```

By default, Heading 2 starts a slide. A different heading level can be selected with `--slide-heading-level`.

## Images

Insert images into the Word document using **In Line with Text**. The renderer extracts them into the generated presentation's `media/` folder.

Add meaningful alternative text to informative images in Word. The generated QA report identifies any extracted images for which alternative text was not detected.

## Video and iframe embeds

Place an embed instruction on its own line within the relevant slide.

### YouTube

```text
YouTubeEmbed :: https://www.youtube.com/watch?v=VIDEO_ID
```

The following forms are also supported:

```text
[YOUTUBE] https://youtu.be/VIDEO_ID
```

or:

```text
[YOUTUBE]
https://www.youtube.com/watch?v=VIDEO_ID
```

### Panopto

```text
PanoptoEmbed :: https://example.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=SESSION_ID
```

The renderer converts supported Panopto Viewer URLs to Embed URLs while preserving the original Panopto host and query string.

### Generic iframe

```text
IFrameEmbed :: https://example.com/embed/
```

The following form is also supported:

```text
[IFRAME]
https://example.com/embed/
```

Only embed content from trusted sources. Some websites prevent iframe embedding through their security settings.

## Run the supplied demonstration

Create the default input folder and copy the sample Word document into it:

```bash
mkdir -p imports/presentations
cp Vaccine_Effectiveness_Slide_Test.docx imports/presentations/
```

Generate the Quarto Markdown presentation and QA report:

```bash
python3 word_to_revealjs.py \
  --input-glob "imports/presentations/**/*.docx" \
  --output-dir "output/presentations"
```

Expected summary:

```text
Title: Introduction to Vaccine Effectiveness
Slides: 8
Images: 1
```

The main outputs are:

```text
output/presentations/Vaccine_Effectiveness_Slide_Test/
├── _quarto.yml
├── Vaccine_Effectiveness_Slide_Test_slides.qmd
├── qa_report_revealjs.md
└── media/
```

## Generate and render the HTML presentation

To convert the Word document and immediately render it:

```bash
python3 word_to_revealjs.py \
  --input-glob "imports/presentations/**/*.docx" \
  --output-dir "output/presentations" \
  --render
```

The rendered presentation will normally be created inside:

```text
output/presentations/Vaccine_Effectiveness_Slide_Test/_site/
```

Alternatively, generate the `.qmd` first and render it separately:

```bash
quarto render \
  "output/presentations/Vaccine_Effectiveness_Slide_Test/Vaccine_Effectiveness_Slide_Test_slides.qmd"
```

## Convert another Word document

Place the document in `imports/presentations/`, then run:

```bash
python3 word_to_revealjs.py \
  --input-glob "imports/presentations/**/*.docx" \
  --output-dir "output/presentations" \
  --render
```

Each Word document receives its own output directory.

## Select a Reveal.js theme

Use `--theme` to select a Quarto Reveal.js theme:

```bash
python3 word_to_revealjs.py \
  --input-glob "imports/presentations/**/*.docx" \
  --output-dir "output/presentations" \
  --theme solarized \
  --render
```

The default theme is `simple`.

## Use a different slide heading level

To use Heading 3 rather than Heading 2 to begin each slide:

```bash
python3 word_to_revealjs.py \
  --input-glob "imports/presentations/**/*.docx" \
  --output-dir "output/presentations" \
  --slide-heading-level h3
```

Supported values are `h1`, `h2`, `h3`, `h4`, `h5` and `h6`.

## Clean the output directory

Use `--clean` to delete the complete output directory before conversion:

```bash
python3 word_to_revealjs.py \
  --input-glob "imports/presentations/**/*.docx" \
  --output-dir "output/presentations" \
  --clean \
  --render
```

Use this option carefully because existing files inside the specified output directory will be removed.

## Command-line options

| Option | Description |
|---|---|
| `--input-glob PATTERN` | DOCX input pattern; default: `imports/presentations/**/*.docx` |
| `--output-dir PATH` | Output directory; default: `output/presentations` |
| `--slide-heading-level LEVEL` | Word heading level used for slides; default: `h2` |
| `--theme NAME` | Reveal.js theme; default: `simple` |
| `--render` | Run `quarto render` after generating each `.qmd` file |
| `--clean` | Delete the complete output directory before conversion |
| `-h`, `--help` | Display command help |

## QA report

Every converted presentation includes `qa_report_revealjs.md`. It records:

- the source document and presentation title;
- the number and titles of slides;
- detected semantic headings;
- the number of extracted images;
- image alternative-text status;
- conversion messages from Mammoth;
- other QA findings.

Review this report and the rendered presentation before publication.

## Troubleshooting

### `No DOCX files found`

Check that the Word document is inside the folder matched by `--input-glob`. Keep the glob pattern in quotation marks so the converter receives it unchanged.

### `No slide sections detected`

Apply the expected Word Heading style to each slide title. By default, slide titles must use **Heading 2**.

### `ModuleNotFoundError`

Activate the virtual environment and reinstall the requirements:

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### `quarto: command not found`

Install Quarto and reopen Terminal, then confirm the installation with:

```bash
quarto --version
```

### Presentation content is too large for a slide

Reduce the amount of content under the relevant Word slide heading or divide it into additional slides. The generated Reveal.js configuration permits scrolling, but concise slide content remains preferable.

### An embedded video does not display

Check the URL and confirm that the provider permits embedding. Panopto access permissions must also allow the intended audience to view the recording.

## Accessibility and quality assurance

Before publication:

- review every generated slide;
- check keyboard navigation;
- add meaningful alternative text to informative images;
- ensure videos include captions or transcripts;
- use descriptive link text;
- check colour contrast;
- avoid overcrowded slides;
- test the presentation at different viewport sizes;
- confirm that embedded services comply with applicable privacy and security requirements.

## Licence

This project is available under the MIT Licence.

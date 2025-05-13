# The End of Dev Confusion: How Grimoire Becomes Your Smartest Teammate

<p align="center">
  <img src="images/logo.svg" alt="Grimoire Logo" width="200"/>
</p>

> An in-depth look at the AI-powered CLI assistant that turns onboarding, debugging, and docs into frictionless workflows.

---

## Lost in the Code Maze?

Imagine joining a codebase that’s been evolving for years—half-documented modules, ad-hoc scripts, scattered READMEs, and a tangle of versioned dependencies. Even veteran engineers find themselves asking:

* “Why is this import here?”
* “Which branch or tag matches our deployed version?”
* “Where did this config live?”

Traditional tools—spray-and-pray greps, copy-pasted StackOverflow snippets, or one-off LLM chats—just can’t internalize your project’s history and custom wiring. The result? Hours wasted context-switching instead of building features.

That’s why we built **Grimoire**.

---

## What Makes Grimoire Different

Grimoire is an open-source, **Retrieval-Augmented Generation (RAG)** CLI that lives alongside your repo. It:

1. **Ingests everything**: source files, Markdown docs, dependency manifests.
2. **Embeds intelligently**: converts code snippets into high-dimensional vectors via your chosen LLM (OpenAI, Mistral, etc.).
3. **Stores locally**: uses PostgreSQL + pgvector for instant similarity lookups.
4. **Answers contextually**: you ask “How does auth flow work?” and get back the exact function, doc-comment, and usage example—all in one snippet.

---

## Try It in Four Commands

1. **Init**

   ```bash
   grim init
   ```

   Choose which folders, file types, and API key to include.

2. **Sync**

   ```bash
   grim sync
   ```

   Parse code + docs, generate embeddings, and populate your vector DB.

3. **Ask**

   ```bash
   grim ask "Where is the payment logic?"
   ```

   Retrieve the most relevant snippets and return a concise, code-grounded answer.

4. **Verify & Add**

   ```bash
   grim verify              # sanity-check your setup  
   grim add --dev tests/fixtures  # ingest new files on the fly  
   ```

> **Pro Tip:** Use `--dev` to include test scripts, migrations, or internal utilities into your RAG index.

---

## Why Your Team Will Love It

* 🚀 **Instant Onboarding**
  New hires run one command instead of reading dozens of docs—answers pop up right in their terminal.
* 🔄 **Zero Context-Switch**
  No more toggling between Slack, JIRA, and your editor; keep your hands on the keys.
* 📚 **Living Docs**
  Every Q\&A session auto-documents itself—exportable as Markdown to embed in your wiki.
* ⚖️ **Scales with You**
  From a 5-person startup to a global team, Grimoire handles repos of any size in seconds.

---

## Under the Hood

Each `grim sync` cycle:

* **Repo Traversal:** walks code, docs, and config files.
* **Chunking & Embedding:** splits into logical units (functions, classes, paragraphs) and vectorizes.
* **Vector Store:** writes into PostgreSQL + pgvector.
* **Similarity Search:** on query, finds top-K nearest vectors and stitches them into your prompt.

---

## Ready to Ditch Dev Confusion?

Grimoire is MIT-licensed and open-source:
[https://github.com/BDP25/grimoire](https://github.com/BDP25/grimoire)

---

**Authors**
Felix Céline (`felixcel`), Kiritharan Kirishana (`kiritkir`), Truninger John (`trunijoh`)

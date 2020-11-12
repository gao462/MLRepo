## Table Of Content

* [File: doc/main.py](#file-docmainpy)
  * [Section: Document Objects](#section-document-objects)
    * [Class: doc.main.Document](#class-docmaindocument)
      * [Function: doc.main.Document.\_\_init\_\_](#function-docmaindocument__init__)
      * [Function: doc.main.Document.notes](#function-docmaindocumentnotes)
  * [Section: File System Document Objects](#section-file-system-document-objects)
    * [Class: doc.main.FileSysDocument](#class-docmainfilesysdocument)
      * [Block: doc.main.FileSysDocument: Define Github con...](#block-docmainfilesysdocument-define-github-con)
      * [Function: doc.main.FileSysDocument.\_\_init\_\_](#function-docmainfilesysdocument__init__)
    * [Class: doc.main.DirectoryDocument](#class-docmaindirectorydocument)
      * [Function: doc.main.DirectoryDocument.\_\_init\_\_](#function-docmaindirectorydocument__init__)
      * [Function: doc.main.DirectoryDocument.parse](#function-docmaindirectorydocumentparse)
      * [Function: doc.main.DirectoryDocument.register](#function-docmaindirectorydocumentregister)
      * [Function: doc.main.DirectoryDocument.notes](#function-docmaindirectorydocumentnotes)
      * [Function: doc.main.DirectoryDocument.root](#function-docmaindirectorydocumentroot)
    * [Class: doc.main.FileDocument](#class-docmainfiledocument)
      * [Function: doc.main.FileDocument.\_\_init\_\_](#function-docmainfiledocument__init__)
      * [Function: doc.main.FileDocument.parse](#function-docmainfiledocumentparse)
      * [Function: doc.main.FileDocument.register\_classes](#function-docmainfiledocumentregister_classes)
      * [Function: doc.main.FileDocument.notes](#function-docmainfiledocumentnotes)
    * [Function: doc.main.toc](#function-docmaintoc)
    * [Function: doc.main.github\_header](#function-docmaingithub_header)
  * [Section: Code Code Document Objects](#section-code-code-document-objects)
    * [Block: doc.main: Hierarchy constants.](#block-docmain-hierarchy-constants)
    * [Class: doc.main.CodeDocument](#class-docmaincodedocument)
      * [Function: doc.main.CodeDocument.\_\_init\_\_](#function-docmaincodedocument__init__)
      * [Function: doc.main.CodeDocument.allocate](#function-docmaincodedocumentallocate)
      * [Function: doc.main.CodeDocument.parse](#function-docmaincodedocumentparse)
  * [Section: Global Code Document Objects](#section-global-code-document-objects)
    * [Class: doc.main.ModuleDocument](#class-docmainmoduledocument)
      * [Function: doc.main.ModuleDocument.allocate](#function-docmainmoduledocumentallocate)
      * [Function: doc.main.ModuleDocument.parse](#function-docmainmoduledocumentparse)
      * [Function: doc.main.ModuleDocument.notes](#function-docmainmoduledocumentnotes)
    * [Class: doc.main.GlobalDocument](#class-docmainglobaldocument)
      * [Function: doc.main.GlobalDocument.allocate](#function-docmainglobaldocumentallocate)
      * [Function: doc.main.GlobalDocument.parse](#function-docmainglobaldocumentparse)
      * [Function: doc.main.GlobalDocument.notes](#function-docmainglobaldocumentnotes)
  * [Section: Series Code Document Objects](#section-series-code-document-objects)
    * [Class: doc.main.SeriesDocument](#class-docmainseriesdocument)
      * [Function: doc.main.SeriesDocument.allocate](#function-docmainseriesdocumentallocate)
      * [Function: doc.main.SeriesDocument.parse](#function-docmainseriesdocumentparse)
      * [Function: doc.main.SeriesDocument.dedent](#function-docmainseriesdocumentdedent)
      * [Function: doc.main.SeriesDocument.notes](#function-docmainseriesdocumentnotes)
  * [Section: Class Code Document Objects](#section-class-code-document-objects)
    * [Class: doc.main.ClassDocument](#class-docmainclassdocument)
      * [Function: doc.main.ClassDocument.allocate](#function-docmainclassdocumentallocate)
      * [Function: doc.main.ClassDocument.parse](#function-docmainclassdocumentparse)
      * [Function: doc.main.ClassDocument.notes](#function-docmainclassdocumentnotes)
      * [Function: doc.main.ClassDocument.check\_inheritance](#function-docmainclassdocumentcheck_inheritance)
    * [Function: doc.main.func\_consistency](#function-docmainfunc_consistency)
    * [Function: doc.main.is\_subparagraphs](#function-docmainis_subparagraphs)
    * [Function: doc.main.is\_subdefs](#function-docmainis_subdefs)
    * [Function: doc.main.order\_key\_argbreak](#function-docmainorder_key_argbreak)
  * [Section: Function Code Document Objects](#section-function-code-document-objects)
    * [Class: doc.main.FunctionDocument](#class-docmainfunctiondocument)
      * [Function: doc.main.FunctionDocument.allocate](#function-docmainfunctiondocumentallocate)
      * [Function: doc.main.FunctionDocument.parse](#function-docmainfunctiondocumentparse)
      * [Function: doc.main.FunctionDocument.notes](#function-docmainfunctiondocumentnotes)
  * [Section: Operation Block Code Document Objects](#section-operation-block-code-document-objects)
    * [Class: doc.main.OPBlockDocument](#class-docmainopblockdocument)
      * [Block: doc.main.OPBlockDocument: Define constants.](#block-docmainopblockdocument-define-constants)
      * [Function: doc.main.OPBlockDocument.allocate](#function-docmainopblockdocumentallocate)
      * [Function: doc.main.OPBlockDocument.parse](#function-docmainopblockdocumentparse)
      * [Function: doc.main.OPBlockDocument.notes](#function-docmainopblockdocumentnotes)
  * [Section: Function Code Document Objects](#section-function-code-document-objects)
    * [Class: doc.main.TypeHintDocument](#class-docmaintypehintdocument)
      * [Function: doc.main.TypeHintDocument.allocate](#function-docmaintypehintdocumentallocate)
      * [Function: doc.main.TypeHintDocument.parse](#function-docmaintypehintdocumentparse)
      * [Function: doc.main.TypeHintDocument.parse\_type](#function-docmaintypehintdocumentparse_type)
      * [Function: doc.main.TypeHintDocument.text](#function-docmaintypehintdocumenttext)
    * [Class: doc.main.ArgumentDocument](#class-docmainargumentdocument)
      * [Function: doc.main.ArgumentDocument.\_\_init\_\_](#function-docmainargumentdocument__init__)
      * [Function: doc.main.ArgumentDocument.allocate](#function-docmainargumentdocumentallocate)
      * [Function: doc.main.ArgumentDocument.parse](#function-docmainargumentdocumentparse)
  * [Section: Block Code Document Objects](#section-block-code-document-objects)
    * [Class: doc.main.BlockDocument](#class-docmainblockdocument)
      * [Function: doc.main.BlockDocument.allocate](#function-docmainblockdocumentallocate)
      * [Function: doc.main.BlockDocument.allocate\_statements](#function-docmainblockdocumentallocate_statements)
      * [Function: doc.main.BlockDocument.parse](#function-docmainblockdocumentparse)
      * [Function: doc.main.BlockDocument.parse\_statements](#function-docmainblockdocumentparse_statements)
    * [Class: doc.main.ImportBlockDocument](#class-docmainimportblockdocument)
      * [Function: doc.main.ImportBlockDocument.allocate\_statements](#function-docmainimportblockdocumentallocate_statements)
      * [Function: doc.main.ImportBlockDocument.parse\_statements](#function-docmainimportblockdocumentparse_statements)
      * [Function: doc.main.ImportBlockDocument.eob](#function-docmainimportblockdocumenteob)
      * [Function: doc.main.ImportBlockDocument.notes](#function-docmainimportblockdocumentnotes)
      * [Function: doc.main.ImportBlockDocument.check](#function-docmainimportblockdocumentcheck)
    * [Class: doc.main.ConstBlockDocument](#class-docmainconstblockdocument)
      * [Function: doc.main.ConstBlockDocument.\_\_init\_\_](#function-docmainconstblockdocument__init__)
      * [Function: doc.main.ConstBlockDocument.allocate](#function-docmainconstblockdocumentallocate)
      * [Function: doc.main.ConstBlockDocument.parse](#function-docmainconstblockdocumentparse)
      * [Function: doc.main.ConstBlockDocument.notes](#function-docmainconstblockdocumentnotes)
  * [Section: Statement Code Document Objects](#section-statement-code-document-objects)
    * [Class: doc.main.CommentDocument](#class-docmaincommentdocument)
      * [Function: doc.main.CommentDocument.allocate](#function-docmaincommentdocumentallocate)
      * [Function: doc.main.CommentDocument.parse](#function-docmaincommentdocumentparse)
      * [Function: doc.main.CommentDocument.translate](#function-docmaincommentdocumenttranslate)
      * [Function: doc.main.CommentDocument.notes](#function-docmaincommentdocumentnotes)
    * [Class: doc.main.ImportDocument](#class-docmainimportdocument)
      * [Function: doc.main.ImportDocument.allocate](#function-docmainimportdocumentallocate)
      * [Function: doc.main.ImportDocument.parse](#function-docmainimportdocumentparse)
      * [Function: doc.main.ImportDocument.parse\_import](#function-docmainimportdocumentparse_import)
      * [Function: doc.main.ImportDocument.parse\_from](#function-docmainimportdocumentparse_from)
      * [Function: doc.main.ImportDocument.parse\_module](#function-docmainimportdocumentparse_module)
      * [Function: doc.main.ImportDocument.parse\_identifier](#function-docmainimportdocumentparse_identifier)
      * [Function: doc.main.ImportDocument.parse\_rename](#function-docmainimportdocumentparse_rename)
      * [Function: doc.main.ImportDocument.append\_module](#function-docmainimportdocumentappend_module)
      * [Function: doc.main.ImportDocument.append\_identifier](#function-docmainimportdocumentappend_identifier)
      * [Function: doc.main.ImportDocument.notes](#function-docmainimportdocumentnotes)
    * [Class: doc.main.IntroDocument](#class-docmainintrodocument)
      * [Function: doc.main.IntroDocument.translate](#function-docmainintrodocumenttranslate)
      * [Function: doc.main.IntroDocument.notes](#function-docmainintrodocumentnotes)
    * [Class: doc.main.DescriptionDocument](#class-docmaindescriptiondocument)
      * [Function: doc.main.DescriptionDocument.allocate](#function-docmaindescriptiondocumentallocate)
      * [Function: doc.main.DescriptionDocument.parse](#function-docmaindescriptiondocumentparse)
      * [Function: doc.main.DescriptionDocument.decode](#function-docmaindescriptiondocumentdecode)
    * [Class: doc.main.ClassDescDocument](#class-docmainclassdescdocument)
      * [Function: doc.main.ClassDescDocument.allocate](#function-docmainclassdescdocumentallocate)
      * [Function: doc.main.ClassDescDocument.decode](#function-docmainclassdescdocumentdecode)
    * [Class: doc.main.FuncDescDocument](#class-docmainfuncdescdocument)
      * [Function: doc.main.FuncDescDocument.decode](#function-docmainfuncdescdocumentdecode)
      * [Function: doc.main.FuncDescDocument.review](#function-docmainfuncdescdocumentreview)
      * [Function: doc.main.FuncDescDocument.review\_args](#function-docmainfuncdescdocumentreview_args)
      * [Function: doc.main.FuncDescDocument.review\_returns](#function-docmainfuncdescdocumentreview_returns)
  * [Section: Main](#section-main)
    * [Block: doc.main: Main branch.](#block-docmain-main-branch)
* [File: doc/code.py](#file-doccodepy)
  * [Section: Code Objects](#section-code-objects)
    * [Class: doc.code.Word](#class-doccodeword)
      * [Function: doc.code.Word.set](#function-doccodewordset)
      * [Function: doc.code.Word.position](#function-doccodewordposition)
      * [Function: doc.code.Word.check](#function-doccodewordcheck)
    * [Class: doc.code.Line](#class-doccodeline)
      * [Function: doc.code.Line.set](#function-doccodelineset)
      * [Function: doc.code.Line.append](#function-doccodelineappend)
      * [Function: doc.code.Line.reset](#function-doccodelinereset)
      * [Function: doc.code.Line.check](#function-doccodelinecheck)
      * [Function: doc.code.Line.match](#function-doccodelinematch)
      * [Function: doc.code.Line.get](#function-doccodelineget)
      * [Function: doc.code.Line.next](#function-doccodelinenext)
      * [Function: doc.code.Line.eol](#function-doccodelineeol)
    * [Block: doc.code: Define essential...](#block-doccode-define-essential)
    * [Block: doc.code: Define single wor...](#block-doccode-define-single-wor)
    * [Block: doc.code: Overwrite compose...](#block-doccode-overwrite-compose)
    * [Block: doc.code: Define not-word w...](#block-doccode-define-not-word-w)
    * [Block: doc.code: Define sentence w...](#block-doccode-define-sentence-w)
    * [Block: doc.code: Define sentence r...](#block-doccode-define-sentence-r)
    * [Class: doc.code.Code](#class-doccodecode)
      * [Function: doc.code.Code.\_\_init\_\_](#function-doccodecode__init__)
      * [Function: doc.code.Code.load\_file](#function-doccodecodeload_file)
      * [Function: doc.code.Code.load\_texts](#function-doccodecodeload_texts)
      * [Function: doc.code.Code.load\_tokens](#function-doccodecodeload_tokens)
      * [Function: doc.code.Code.rule\_texts](#function-doccodecoderule_texts)
      * [Function: doc.code.Code.review](#function-doccodecodereview)
      * [Function: doc.code.Code.clear\_space\_until](#function-doccodecodeclear_space_until)
      * [Function: doc.code.Code.clear\_string](#function-doccodecodeclear_string)
      * [Function: doc.code.Code.clear\_common](#function-doccodecodeclear_common)
      * [Function: doc.code.Code.recoverable](#function-doccodecoderecoverable)
      * [Function: doc.code.Code.reset](#function-doccodecodereset)
      * [Function: doc.code.Code.get](#function-doccodecodeget)
      * [Function: doc.code.Code.next](#function-doccodecodenext)
      * [Function: doc.code.Code.eof](#function-doccodecodeeof)
      * [Function: doc.code.Code.blank\_top](#function-doccodecodeblank_top)
      * [Function: doc.code.Code.blank\_next](#function-doccodecodeblank_next)
    * [Function: doc.code.line\_rule\_length](#function-doccodeline_rule_length)
    * [Function: doc.code.line\_rule\_char](#function-doccodeline_rule_char)
    * [Function: doc.code.line\_rule\_break](#function-doccodeline_rule_break)
    * [Function: doc.code.recover](#function-doccoderecover)
    * [Function: doc.code.paragraphize](#function-doccodeparagraphize)
    * [Function: doc.code.mathize](#function-doccodemathize)
    * [Function: doc.code.codize](#function-doccodecodize)
    * [Function: doc.code.textize](#function-doccodetextize)

---

## File: doc/main.py

* [Section: Document Objects](#section-document-objects)
  * [Class: doc.main.Document](#class-docmaindocument)
    * [Function: doc.main.Document.\_\_init\_\_](#function-docmaindocument__init__)
    * [Function: doc.main.Document.notes](#function-docmaindocumentnotes)
* [Section: File System Document Objects](#section-file-system-document-objects)
  * [Class: doc.main.FileSysDocument](#class-docmainfilesysdocument)
    * [Block: doc.main.FileSysDocument: Define Github con...](#block-docmainfilesysdocument-define-github-con)
    * [Function: doc.main.FileSysDocument.\_\_init\_\_](#function-docmainfilesysdocument__init__)
  * [Class: doc.main.DirectoryDocument](#class-docmaindirectorydocument)
    * [Function: doc.main.DirectoryDocument.\_\_init\_\_](#function-docmaindirectorydocument__init__)
    * [Function: doc.main.DirectoryDocument.parse](#function-docmaindirectorydocumentparse)
    * [Function: doc.main.DirectoryDocument.register](#function-docmaindirectorydocumentregister)
    * [Function: doc.main.DirectoryDocument.notes](#function-docmaindirectorydocumentnotes)
    * [Function: doc.main.DirectoryDocument.root](#function-docmaindirectorydocumentroot)
  * [Class: doc.main.FileDocument](#class-docmainfiledocument)
    * [Function: doc.main.FileDocument.\_\_init\_\_](#function-docmainfiledocument__init__)
    * [Function: doc.main.FileDocument.parse](#function-docmainfiledocumentparse)
    * [Function: doc.main.FileDocument.register\_classes](#function-docmainfiledocumentregister_classes)
    * [Function: doc.main.FileDocument.notes](#function-docmainfiledocumentnotes)
  * [Function: doc.main.toc](#function-docmaintoc)
  * [Function: doc.main.github\_header](#function-docmaingithub_header)
* [Section: Code Code Document Objects](#section-code-code-document-objects)
  * [Block: doc.main: Hierarchy constants.](#block-docmain-hierarchy-constants)
  * [Class: doc.main.CodeDocument](#class-docmaincodedocument)
    * [Function: doc.main.CodeDocument.\_\_init\_\_](#function-docmaincodedocument__init__)
    * [Function: doc.main.CodeDocument.allocate](#function-docmaincodedocumentallocate)
    * [Function: doc.main.CodeDocument.parse](#function-docmaincodedocumentparse)
* [Section: Global Code Document Objects](#section-global-code-document-objects)
  * [Class: doc.main.ModuleDocument](#class-docmainmoduledocument)
    * [Function: doc.main.ModuleDocument.allocate](#function-docmainmoduledocumentallocate)
    * [Function: doc.main.ModuleDocument.parse](#function-docmainmoduledocumentparse)
    * [Function: doc.main.ModuleDocument.notes](#function-docmainmoduledocumentnotes)
  * [Class: doc.main.GlobalDocument](#class-docmainglobaldocument)
    * [Function: doc.main.GlobalDocument.allocate](#function-docmainglobaldocumentallocate)
    * [Function: doc.main.GlobalDocument.parse](#function-docmainglobaldocumentparse)
    * [Function: doc.main.GlobalDocument.notes](#function-docmainglobaldocumentnotes)
* [Section: Series Code Document Objects](#section-series-code-document-objects)
  * [Class: doc.main.SeriesDocument](#class-docmainseriesdocument)
    * [Function: doc.main.SeriesDocument.allocate](#function-docmainseriesdocumentallocate)
    * [Function: doc.main.SeriesDocument.parse](#function-docmainseriesdocumentparse)
    * [Function: doc.main.SeriesDocument.dedent](#function-docmainseriesdocumentdedent)
    * [Function: doc.main.SeriesDocument.notes](#function-docmainseriesdocumentnotes)
* [Section: Class Code Document Objects](#section-class-code-document-objects)
  * [Class: doc.main.ClassDocument](#class-docmainclassdocument)
    * [Function: doc.main.ClassDocument.allocate](#function-docmainclassdocumentallocate)
    * [Function: doc.main.ClassDocument.parse](#function-docmainclassdocumentparse)
    * [Function: doc.main.ClassDocument.notes](#function-docmainclassdocumentnotes)
    * [Function: doc.main.ClassDocument.check\_inheritance](#function-docmainclassdocumentcheck_inheritance)
  * [Function: doc.main.func\_consistency](#function-docmainfunc_consistency)
  * [Function: doc.main.is\_subparagraphs](#function-docmainis_subparagraphs)
  * [Function: doc.main.is\_subdefs](#function-docmainis_subdefs)
  * [Function: doc.main.order\_key\_argbreak](#function-docmainorder_key_argbreak)
* [Section: Function Code Document Objects](#section-function-code-document-objects)
  * [Class: doc.main.FunctionDocument](#class-docmainfunctiondocument)
    * [Function: doc.main.FunctionDocument.allocate](#function-docmainfunctiondocumentallocate)
    * [Function: doc.main.FunctionDocument.parse](#function-docmainfunctiondocumentparse)
    * [Function: doc.main.FunctionDocument.notes](#function-docmainfunctiondocumentnotes)
* [Section: Operation Block Code Document Objects](#section-operation-block-code-document-objects)
  * [Class: doc.main.OPBlockDocument](#class-docmainopblockdocument)
    * [Block: doc.main.OPBlockDocument: Define constants.](#block-docmainopblockdocument-define-constants)
    * [Function: doc.main.OPBlockDocument.allocate](#function-docmainopblockdocumentallocate)
    * [Function: doc.main.OPBlockDocument.parse](#function-docmainopblockdocumentparse)
    * [Function: doc.main.OPBlockDocument.notes](#function-docmainopblockdocumentnotes)
* [Section: Function Code Document Objects](#section-function-code-document-objects)
  * [Class: doc.main.TypeHintDocument](#class-docmaintypehintdocument)
    * [Function: doc.main.TypeHintDocument.allocate](#function-docmaintypehintdocumentallocate)
    * [Function: doc.main.TypeHintDocument.parse](#function-docmaintypehintdocumentparse)
    * [Function: doc.main.TypeHintDocument.parse\_type](#function-docmaintypehintdocumentparse_type)
    * [Function: doc.main.TypeHintDocument.text](#function-docmaintypehintdocumenttext)
  * [Class: doc.main.ArgumentDocument](#class-docmainargumentdocument)
    * [Function: doc.main.ArgumentDocument.\_\_init\_\_](#function-docmainargumentdocument__init__)
    * [Function: doc.main.ArgumentDocument.allocate](#function-docmainargumentdocumentallocate)
    * [Function: doc.main.ArgumentDocument.parse](#function-docmainargumentdocumentparse)
* [Section: Block Code Document Objects](#section-block-code-document-objects)
  * [Class: doc.main.BlockDocument](#class-docmainblockdocument)
    * [Function: doc.main.BlockDocument.allocate](#function-docmainblockdocumentallocate)
    * [Function: doc.main.BlockDocument.allocate\_statements](#function-docmainblockdocumentallocate_statements)
    * [Function: doc.main.BlockDocument.parse](#function-docmainblockdocumentparse)
    * [Function: doc.main.BlockDocument.parse\_statements](#function-docmainblockdocumentparse_statements)
  * [Class: doc.main.ImportBlockDocument](#class-docmainimportblockdocument)
    * [Function: doc.main.ImportBlockDocument.allocate\_statements](#function-docmainimportblockdocumentallocate_statements)
    * [Function: doc.main.ImportBlockDocument.parse\_statements](#function-docmainimportblockdocumentparse_statements)
    * [Function: doc.main.ImportBlockDocument.eob](#function-docmainimportblockdocumenteob)
    * [Function: doc.main.ImportBlockDocument.notes](#function-docmainimportblockdocumentnotes)
    * [Function: doc.main.ImportBlockDocument.check](#function-docmainimportblockdocumentcheck)
  * [Class: doc.main.ConstBlockDocument](#class-docmainconstblockdocument)
    * [Function: doc.main.ConstBlockDocument.\_\_init\_\_](#function-docmainconstblockdocument__init__)
    * [Function: doc.main.ConstBlockDocument.allocate](#function-docmainconstblockdocumentallocate)
    * [Function: doc.main.ConstBlockDocument.parse](#function-docmainconstblockdocumentparse)
    * [Function: doc.main.ConstBlockDocument.notes](#function-docmainconstblockdocumentnotes)
* [Section: Statement Code Document Objects](#section-statement-code-document-objects)
  * [Class: doc.main.CommentDocument](#class-docmaincommentdocument)
    * [Function: doc.main.CommentDocument.allocate](#function-docmaincommentdocumentallocate)
    * [Function: doc.main.CommentDocument.parse](#function-docmaincommentdocumentparse)
    * [Function: doc.main.CommentDocument.translate](#function-docmaincommentdocumenttranslate)
    * [Function: doc.main.CommentDocument.notes](#function-docmaincommentdocumentnotes)
  * [Class: doc.main.ImportDocument](#class-docmainimportdocument)
    * [Function: doc.main.ImportDocument.allocate](#function-docmainimportdocumentallocate)
    * [Function: doc.main.ImportDocument.parse](#function-docmainimportdocumentparse)
    * [Function: doc.main.ImportDocument.parse\_import](#function-docmainimportdocumentparse_import)
    * [Function: doc.main.ImportDocument.parse\_from](#function-docmainimportdocumentparse_from)
    * [Function: doc.main.ImportDocument.parse\_module](#function-docmainimportdocumentparse_module)
    * [Function: doc.main.ImportDocument.parse\_identifier](#function-docmainimportdocumentparse_identifier)
    * [Function: doc.main.ImportDocument.parse\_rename](#function-docmainimportdocumentparse_rename)
    * [Function: doc.main.ImportDocument.append\_module](#function-docmainimportdocumentappend_module)
    * [Function: doc.main.ImportDocument.append\_identifier](#function-docmainimportdocumentappend_identifier)
    * [Function: doc.main.ImportDocument.notes](#function-docmainimportdocumentnotes)
  * [Class: doc.main.IntroDocument](#class-docmainintrodocument)
    * [Function: doc.main.IntroDocument.translate](#function-docmainintrodocumenttranslate)
    * [Function: doc.main.IntroDocument.notes](#function-docmainintrodocumentnotes)
  * [Class: doc.main.DescriptionDocument](#class-docmaindescriptiondocument)
    * [Function: doc.main.DescriptionDocument.allocate](#function-docmaindescriptiondocumentallocate)
    * [Function: doc.main.DescriptionDocument.parse](#function-docmaindescriptiondocumentparse)
    * [Function: doc.main.DescriptionDocument.decode](#function-docmaindescriptiondocumentdecode)
  * [Class: doc.main.ClassDescDocument](#class-docmainclassdescdocument)
    * [Function: doc.main.ClassDescDocument.allocate](#function-docmainclassdescdocumentallocate)
    * [Function: doc.main.ClassDescDocument.decode](#function-docmainclassdescdocumentdecode)
  * [Class: doc.main.FuncDescDocument](#class-docmainfuncdescdocument)
    * [Function: doc.main.FuncDescDocument.decode](#function-docmainfuncdescdocumentdecode)
    * [Function: doc.main.FuncDescDocument.review](#function-docmainfuncdescdocumentreview)
    * [Function: doc.main.FuncDescDocument.review\_args](#function-docmainfuncdescdocumentreview_args)
    * [Function: doc.main.FuncDescDocument.review\_returns](#function-docmainfuncdescdocumentreview_returns)
* [Section: Main](#section-main)
  * [Block: doc.main: Main branch.](#block-docmain-main-branch)

## Section: Document Objects

Prototype of document. It also includes prototype for file system document and real code document.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.Document

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L42)

- Super: object

Document prototype.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.Document.\_\_init\_\_](#function-docmaindocument__init__)
  * [Function: doc.main.Document.notes](#function-docmaindocumentnotes)

---

### Function: doc.main.Document.\_\_init\_\_

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L46)

Initialize.

> **Arguments**
> - *self*: `Document`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Allocate notes buffer.
> self.markdown: List[str] = []
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindocument)

---

### Function: doc.main.Document.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L63)

Generate notes.

> **Arguments**
> - *self*: `Document`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Prototype may not implement everything.
> error("Function is not implemented.")
> raise NotImplementedError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindocument)

## Section: File System Document Objects

Documentize tokenized code files, and check style rules in the meanwhile.

In this level, a document directory controller will traverse every folder in MLRepo. At each folder, controller will identify all python files, and generate their markdown notes by their file controllers. Generated notes is then merged into README file inside current directory.

In the README file, super links to exact Github code position are also created for global or global-class level classes, functions, and blocks. Styled code snaps for those parts are also attached with them.

For function or class inside a function, local-class or branch-of-block, it will be compressed into its name definition. Arguments or codes of it will be replaced by "..." which can be used as python ellipsis for code.

After the generation, a strict description matching is applied on classes with inheritance relationships so that inherited classes only extends function argument names and description details of inheriting classes. This also autofills the exact Github code positions for module imports and classes.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.FileSysDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L116)

- Super: [doc.main.Document](#class-docmaindocument)

Document for file system prototype.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Block: doc.main.FileSysDocument: Define Github con...](#block-docmainfilesysdocument-define-github-con)
  * [Function: doc.main.FileSysDocument.\_\_init\_\_](#function-docmainfilesysdocument__init__)

---

### Block: doc.main.FileSysDocument: Define Github con...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L120)

> ```python
> # Define Github constants.
> PROJECT = "MLRepo"
> FOLDER = "/u/antor/u12/gao462/{:s}".format(PROJECT)
> GITHUB = "https://github.com/gao462/{:s}".format(PROJECT)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfilesysdocument)

---

### Function: doc.main.FileSysDocument.\_\_init\_\_

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L125)

Initialize.

> **Arguments**
> - *self*: `Document`
>
> - *path*: `str`
>
>   Path of this document.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> Document.__init__(self, *args, **kargs)
>
> # Save necessary attributes
> self.PATH = path
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfilesysdocument)

---

## Class: doc.main.DirectoryDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L150)

- Super: [doc.main.FileSysDocument](#class-docmainfilesysdocument)

Document for a directory.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.DirectoryDocument.\_\_init\_\_](#function-docmaindirectorydocument__init__)
  * [Function: doc.main.DirectoryDocument.parse](#function-docmaindirectorydocumentparse)
  * [Function: doc.main.DirectoryDocument.register](#function-docmaindirectorydocumentregister)
  * [Function: doc.main.DirectoryDocument.notes](#function-docmaindirectorydocumentnotes)
  * [Function: doc.main.DirectoryDocument.root](#function-docmaindirectorydocumentroot)

---

### Function: doc.main.DirectoryDocument.\_\_init\_\_

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L154)

Initialize.

> **Arguments**
> - *self*: `DirectoryDocument`
>
> - *path*: `str`
>
>   Path of this document.
>
> - *\*args*: `object`
>
> - *rootdoc*: `Union[DirectoryDocument, None]`
>
>   Document for root directory.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> FileSysDocument.__init__(self, path, *args, **kargs)
>
> # Save necessary attributes.
> self.ROOTDOC = self if rootdoc is None else rootdoc
>
> # File system should trace definitions.
> self.classes: Dict[str, str] = {}
> self.classdocs: Dict[str, ClassDocument] = {}
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindirectorydocument)

---

### Function: doc.main.DirectoryDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L185)

Parse content.

> **Arguments**
> - *self*: `DirectoryDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Traverse the tree.
> self.subdirs = []
> self.files = []
> for itr in os.listdir(self.PATH):
>     itr = os.path.join(self.PATH, itr)
>     if (os.path.isdir(itr)):
>         base = os.path.basename(itr)
>         if (base == "__pycache__"):
>             # Some directory name should be ignored.
>             pass
>         elif (base[0] == "."):
>             # Hidden directory should be ignored.
>             pass
>         else:
>             dirdoc = DirectoryDocument(itr, rootdoc=self.ROOTDOC)
>             dirdoc.parse()
>             self.subdirs.append(dirdoc)
>     elif (os.path.isfile(itr)):
>         base, ext = os.path.splitext(itr)
>         base = os.path.basename(base)
>         if (ext == ".py"):
>             if (base == "__init__"):
>                 warning("Skip \"{:s}\" for now.".format(itr))
>             else:
>                 filedoc = FileDocument(itr, rootdoc=self)
>                 filedoc.parse()
>                 self.files.append(filedoc)
>         elif (ext in (".md", ".sh")):
>             # Some extension name should be ignored.
>             pass
>         elif (base == ".gitignore"):
>             # Some no-extension file should be ignored.
>             pass
>         else:
>             error(
>                 "At \"{:s}\", expect a python/Markdown/bash/Git file.",
>                 itr,
>             )
>             raise RuntimeError
>     else:
>         error(
>             "At \"{:s}\", expect a directory/file.",
>             itr,
>         )
>         raise RuntimeError
>
> # Register all definitions from documents in the tree.
> self.register()
>
> # Root specific operations.
> if (self.PATH == self.FOLDER):
>     self.root()
> else:
>     pass
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindirectorydocument)

---

### Function: doc.main.DirectoryDocument.register

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L254)

Register definitions.

> **Arguments**
> - *self*: `DirectoryDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Register definitions from sub directories.
> for dirdoc in self.subdirs:
>     for key, location in dirdoc.classes.items():
>         self.classes[key] = location
>     for key, holder in dirdoc.classdocs.items():
>         self.classdocs[key] = holder
>
> # Register definitions from files.
> for filedoc in self.files:
>     for key, row in filedoc.classes.items():
>         location = "{:s}/blob/master/{:s}{:s}".format(
>             self.GITHUB, filedoc.PATH, row,
>         )
>         self.classes["{:s}.{:s}".format(filedoc.ME, key)] = location
>     for key, holder in filedoc.classdocs.items():
>         self.classdocs["{:s}.{:s}".format(filedoc.ME, key)] = holder
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindirectorydocument)

---

### Function: doc.main.DirectoryDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L287)

Generate notes.

> **Arguments**
> - *self*: `DirectoryDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Generate sub directory notes.
> for dirdoc in self.subdirs:
>     dirdoc.notes()
>
> # Generate file notes
> for filedoc in self.files:
>     filedoc.notes()
>     self.markdown.extend(["", "---", ""])
>     self.markdown.extend(filedoc.markdown)
>
> # Generate table of content.
> self.markdown = toc(self.markdown) + self.markdown
>
> # Save markdown note as README.
> file = open(os.path.join(self.PATH, "README.md"), "w")
> file.write("\n".join(self.markdown))
> file.close()
>
> # Clear children notes for memory efficency.
> for filedoc in self.files:
>     filedoc.markdown.clear()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindirectorydocument)

---

### Function: doc.main.DirectoryDocument.root

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L326)

Root specific operations.

> **Arguments**
> - *self*: `DirectoryDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Generate notes.
> self.notes()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindirectorydocument)

---

## Class: doc.main.FileDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L344)

- Super: [doc.main.FileSysDocument](#class-docmainfilesysdocument)

Document for a file.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.FileDocument.\_\_init\_\_](#function-docmainfiledocument__init__)
  * [Function: doc.main.FileDocument.parse](#function-docmainfiledocumentparse)
  * [Function: doc.main.FileDocument.register\_classes](#function-docmainfiledocumentregister_classes)
  * [Function: doc.main.FileDocument.notes](#function-docmainfiledocumentnotes)

---

### Function: doc.main.FileDocument.\_\_init\_\_

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L348)

Initialize.

> **Arguments**
> - *self*: `FileDocument`
>
> - *path*: `str`
>
>   Path of this document.
>
> - *\*args*: `object`
>
> - *rootdoc*: `Union[DirectoryDocument, None]`
>
>   Document for root directory.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> FileSysDocument.__init__(self, path, *args, **kargs)
>
> # Save necessary attributes.
> self.ROOTDOC = self if rootdoc is None else rootdoc
>
> # Get module path from file path.
> _, self.PATH = self.PATH.split(self.FOLDER)
> self.PATH = self.PATH[1:]
> self.ME = self.PATH.replace(os.path.join(" ", " ")[1:-1], ".")
> self.ME, _ = os.path.splitext(self.ME)
>
> # File system should trace definitions.
> self.classes: Dict[str, str] = {}
> self.classdocs: Dict[str, ClassDocument] = {}
>
> # Set code to parse on.
> self.code = Code()
>
> # File document has a module-import document and a global document.
> self.modules = ModuleDocument(
>     path=self.PATH, level=0, hierarchy=GLOBAL,
>     superior=None, filedoc=self,
> )
> self.sections = GlobalDocument(
>     path=self.PATH, level=0, hierarchy=GLOBAL,
>     superior=None, filedoc=self,
> )
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfiledocument)

---

### Function: doc.main.FileDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L398)

Parse content.

> **Arguments**
> - *self*: `FileDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Load tokenized code and parse it.
> self.code.load_file(self.PATH)
> self.code.reset()
> self.modules.parse(self.code)
> self.sections.parse(self.code)
>
> # Register classes.
> self.register_classes()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfiledocument)

---

### Function: doc.main.FileDocument.register\_classes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L421)

Register defined classes for later consistency check.

> **Arguments**
> - *self*: `FileDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Register defined classes.
> self.classes = {}
> for _, section in self.sections.sections:
>     for component in section.components:
>         if (isinstance(component, ClassDocument)):
>             self.classes[component.name] = "#L{:d}".format(
>                 component.row,
>             )
>             self.classdocs[component.name] = component
>         else:
>             pass
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfiledocument)

---

### Function: doc.main.FileDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L449)

Generate notes.

> **Arguments**
> - *self*: `FileDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Extend notes by global sections.
> self.sections.notes()
> self.markdown.extend(self.sections.markdown)
>
> # Extend notes by module imports.
> self.modules.notes()
>
> # Generate file header and TOC.
> index = [""] + toc(self.markdown)[2:]
> self.markdown = index + [""] + self.markdown
> self.markdown = ["## File: {:s}".format(self.PATH)] + self.markdown
>
> # Clear children notes for memory efficency.
> self.sections.markdown.clear()
> self.modules.markdown.clear()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfiledocument)

---

## Function: doc.main.toc

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L483)

Generate table of content from given notes.

> **Arguments**
> - *notes*: `List[str]`
>
>   Notes.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *toc*: `List[str]`
>
>   Notes for table of content.

> ```python
> # Registrate all headers by Github header reference behavior.
> headers: List[Tuple[int, str, str]] = []
> has_file = False
> has_section = False
> for itr in notes:
>     # Header level matters.
>     level = 0
>     while (level < len(itr) and itr[level] == "#"):
>         level += 1
>     if (level == 0):
>         continue
>     else:
>         pass
>
>     # Get header text.
>     text = itr[level + 1:]
>     refer = text
>
>     # Github reference ignores colorful ASCII even in console.
>     refer = re.sub(r"\033\[[^m]+m", "", refer)
>     refer = github_header(refer)
>     headers.append((level, text, refer))
>     if (len(refer) > 5 and refer[0:5] == "file-"):
>         has_file = True
>     elif (len(refer) > 8 and refer[0:8] == "section-"):
>         has_section = True
>     else:
>         pass
>
> # Generate TOC.
> toc = ["## Table Of Content", ""]
> for level, text, refer in headers:
>     num = level - 2
>     if (len(refer) > 5 and refer[0:5] == "file-"):
>         pass
>     elif (len(refer) > 8 and refer[0:8] == "section-"):
>         num += int(has_file)
>     else:
>         num += (int(has_file) + int(has_section))
>     indent = "  " * num
>     link = "{:s}* [{:s}](#{:s})".format(indent, text, refer)
>     toc.append(link)
> return toc
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Function: doc.main.github\_header

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L545)

Get a Github header reference.

> **Arguments**
> - *text*: `str`
>
>   Header text.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *refer*: `str`
>
>   Reference text.

> ```python
> # Github reference ignores "." or "/".
> refer = text
> refer = re.sub(r"(\.|/)", "", refer).strip()
>
> # Github reference replaces escape characters.
> refer = re.sub(r"\\_", "_", refer)
>
> # Github reference should be lower case concatenated by "-".
> refer = re.sub(r"[^\w]+", "-", refer.lower())
> return refer
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

## Section: Code Code Document Objects

Code document on codes of in a file.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Block: doc.main: Hierarchy constants.

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L584)

> ```python
> # Hierarchy constants.
> GLOBAL = 0
> CLASS = 1
> FUNCTION = 2
> BLOCK = 3
> BRANCH = 4
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.CodeDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L592)

- Super: [doc.main.Document](#class-docmaindocument)

Document for code prototype.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.CodeDocument.\_\_init\_\_](#function-docmaincodedocument__init__)
  * [Function: doc.main.CodeDocument.allocate](#function-docmaincodedocumentallocate)
  * [Function: doc.main.CodeDocument.parse](#function-docmaincodedocumentparse)

---

### Function: doc.main.CodeDocument.\_\_init\_\_

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L596)

Initialize.

> **Arguments**
> - *self*: `CodeDocument`
>
> - *\*args*: `object`
>
> - *level*: `int`
>
>   Indent level.
>
> - *hierarchy*: `int`
>
>   Hierarchy integer.
>
> - *superior*: `Union[CodeDocument, None]`
>
>   Superior code document.
>
> - *filedoc*: `FileDocument`
>
>   Document of the file of the code.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> Document.__init__(self, *args, **kargs)
>
> # Save necessary attributes.
> self.LEVEL = level
> self.HIERARCHY = hierarchy
> self.SUPERIOR = self if superior is None else superior
> self.FILEDOC = filedoc
>
> # Allocate children memory.
> self.allocate()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaincodedocument)

---

### Function: doc.main.CodeDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L635)

Allocate children memory.

> **Arguments**
> - *self*: `CodeDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Prototype may not implement everything.
> error("Function is not implemented.")
> raise NotImplementedError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaincodedocument)

---

### Function: doc.main.CodeDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L653)

Parse information into document.

> **Arguments**
> - *self*: `CodeDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Save necessary attributes.
> self.code = code
> self.row = code.scan + 1
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaincodedocument)

## Section: Global Code Document Objects

Code document on global level. It contains module import document which traces all imported modules and identifiers and broadcasts them to deeper code documents.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.ModuleDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L688)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for module imports.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.ModuleDocument.allocate](#function-docmainmoduledocumentallocate)
  * [Function: doc.main.ModuleDocument.parse](#function-docmainmoduledocumentparse)
  * [Function: doc.main.ModuleDocument.notes](#function-docmainmoduledocumentnotes)

---

### Function: doc.main.ModuleDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L692)

Allocate children memory.

> **Arguments**
> - *self*: `ModuleDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Define constant code text.
> text = (
>     "# Add development library to path.\n" \
>     "if (os.path.basename(os.getcwd()) == \"MLRepo\"):\n" \
>     "    sys.path.append(os.path.join(\".\"))\n" \
>     "else:\n" \
>     "    print(\"Code must strictly work in \\\"MLRepo\\\".\")\n" \
>     "    exit()"
> )
>
> # Modules are constant.
> self.future = ImportBlockDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC,
> )
> self.typing = ImportBlockDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC,
> )
> self.python = ImportBlockDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC,
> )
> self.adding = ConstBlockDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC, constant=text,
> )
> self.logging = ImportBlockDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC,
> )
> self.develop = ImportBlockDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC,
> )
>
> # Allocate buffer to trace imports.
> self.modules: Dict[str, List[str]] = {}
> self.identifiers: Dict[str, str] = {}
> self.mapping: Dict[str, str] = {}
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainmoduledocument)

---

### Function: doc.main.ModuleDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L747)

Parse information into document.

> **Arguments**
> - *self*: `ModuleDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Parse code.
> self.future.parse(self.code)
> self.code.blank_next(1)
> self.typing.parse(self.code)
> self.code.blank_next(1)
> self.python.parse(self.code)
> self.code.blank_next(1)
> self.adding.parse(self.code)
> self.code.blank_next(1)
> self.logging.parse(self.code)
> self.code.blank_next(1)
> self.develop.parse(self.code)
>
> # Some import blocks are strictly required.
> assert (
>     len(self.future.comment.paragraphs) == 1 and
>     len(self.future.comment.paragraphs[0]) == 1 and
>     self.future.comment.paragraphs[0][0] == "Import future."
> )
> assert (
>     len(self.typing.comment.paragraphs) == 1 and
>     len(self.typing.comment.paragraphs[0]) == 1 and
>     self.typing.comment.paragraphs[0][0] == "Import typing."
> )
> assert (
>     len(self.python.comment.paragraphs) == 1 and
>     len(self.python.comment.paragraphs[0]) == 1 and
>     self.python.comment.paragraphs[0][0] == "Import dependencies."
> )
> assert (
>     len(self.logging.comment.paragraphs) == 1 and
>     len(self.logging.comment.paragraphs[0]) == 1 and
>     self.logging.comment.paragraphs[0][0] == "Import logging."
> )
> assert (
>     len(self.develop.comment.paragraphs) == 1 and
>     len(self.develop.comment.paragraphs[0]) == 1 and
>     self.develop.comment.paragraphs[0][0] == "Import dependencies."
> )
>
> # Some import commands are strictly required.
> assert (
>     len(self.future.statements) == 1 and
>     self.future.check(0, "from __future__ import annotations")
> )
> assert (
>     len(self.typing.statements) > 1 and
>     self.typing.check(0, "from typing import Any") and
>     self.typing.check(1, "from typing import Tuple as MultiReturn")
> )
>
> # Some import commands are required except for some files.
> if (self.FILEDOC.ME == "pytorch.logging"):
>     pass
> else:
>     assert (
>         len(self.logging.statements) > 0 and
>         self.logging.check(
>             0,
>             "from pytorch.logging import debug, info1, info2, focus" \
>             ", warning, error",
>         )
>     )
>
> # Merge all imports.
> for child in (
>     self.future, self.typing, self.python, self.logging, self.develop,
> ):
>     for name, members in child.modules.items():
>         if (name in self.modules):
>             pass
>         else:
>             self.modules[name] = []
>         self.modules[name].extend(members)
>     for name, source in child.identifiers.items():
>         self.identifiers[name] = source
>     for rename, name in child.mapping.items():
>         self.mapping[rename] = name
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainmoduledocument)

---

### Function: doc.main.ModuleDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L847)

Generate notes.

> **Arguments**
> - *self*: `ModuleDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Generate the dependencies.
> self.markdown.append(
>     "- Dependent on: {:s}".format(", ".join([
>         "`{:s}`".format(itr) for itr in self.modules.keys()
>     ])),
> )
>
> # Import block just integrates its children notes with blank breaks.
> self.markdown.append("")
> self.markdown.append("  > ```python")
> for child in (
>     self.future, self.typing, self.python, self.adding, self.logging,
>     self.develop,
> ):
>     child.notes()
>     for itr in child.markdown:
>         if (len(itr) == 0):
>             self.markdown.append("  >")
>         else:
>             self.markdown.append("  > {:s}".format(itr))
>     self.markdown.append("  >")
> self.markdown[-1] = "  > ```"
>
> # Clear children notes for memory efficency.
> for child in (
>     self.future, self.typing, self.python, self.adding, self.logging,
>     self.develop,
> ):
>     child.markdown.clear()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainmoduledocument)

---

## Class: doc.main.GlobalDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L895)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for global level codes.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.GlobalDocument.allocate](#function-docmainglobaldocumentallocate)
  * [Function: doc.main.GlobalDocument.parse](#function-docmainglobaldocumentparse)
  * [Function: doc.main.GlobalDocument.notes](#function-docmainglobaldocumentnotes)

---

### Function: doc.main.GlobalDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L899)

Allocate children memory.

> **Arguments**
> - *self*: `GlobalDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Children are a list of introductions and sections.
> self.sections: List[Tuple[IntroDocument, SeriesDocument]] = []
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainglobaldocument)

---

### Function: doc.main.GlobalDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L916)

Parse information into document.

> **Arguments**
> - *self*: `GlobalDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Parse introduction and code series until EOF.
> while (not self.code.eof()):
>     # Allocate and append first.
>     intro = IntroDocument(
>         level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>         filedoc=self.FILEDOC,
>     )
>     series = SeriesDocument(
>         level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>         filedoc=self.FILEDOC,
>     )
>     self.sections.append((intro, series))
>
>     # Parse code.
>     self.code.blank_next(2)
>     intro.parse(self.code)
>     self.code.blank_next(2)
>     series.parse(self.code)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainglobaldocument)

---

### Function: doc.main.GlobalDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L956)

Generate notes.

> **Arguments**
> - *self*: `GlobalDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Block notes is just a list of its statments notes.
> first = True
> for intro, series in self.sections:
>     intro.notes()
>     series.notes()
>     if (first):
>         first = False
>     else:
>         self.markdown.append("")
>     self.markdown.extend(intro.markdown)
>     self.markdown.append("")
>     self.markdown.extend(series.markdown)
>
> # Clear children notes for memory efficency.
> for intro, series in self.sections:
>     intro.notes()
>     series.markdown.clear()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainglobaldocument)

## Section: Series Code Document Objects

Code document for a series of codes. It works as a midterm contatenation for class definitions, function definitions and code blocks with the same indent level, thus it contains nothing in memory except a list of documents attached to it.

It will mutually import with ClassDocument, FunctionDocument, OPBlockDocument. Thus, they four are aggregated together in this file.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.SeriesDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1009)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a series of code.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.SeriesDocument.allocate](#function-docmainseriesdocumentallocate)
  * [Function: doc.main.SeriesDocument.parse](#function-docmainseriesdocumentparse)
  * [Function: doc.main.SeriesDocument.dedent](#function-docmainseriesdocumentdedent)
  * [Function: doc.main.SeriesDocument.notes](#function-docmainseriesdocumentnotes)

---

### Function: doc.main.SeriesDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1013)

Allocate children memory.

> **Arguments**
> - *self*: `SeriesDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Children are a list of classes, functions or operation blocks.
> self.components: List[Union[
>     ClassDocument, FunctionDocument, OPBlockDocument,
> ]] = []
>
> # Number of blank breaks is based on hierarchy.
> self.NUM_BLANKS = 1 + int(self.HIERARCHY == GLOBAL)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainseriesdocument)

---

### Function: doc.main.SeriesDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1035)

Parse information into document.

> **Arguments**
> - *self*: `SeriesDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Parse components until dedent.
> first = True
> while (not self.dedent()):
>     # Move blank lines first except for the first time.
>     if (first):
>         first = False
>     else:
>         self.code.blank_next(self.NUM_BLANKS)
>
>     # Allocate according to keyword and append.
>     keyword = self.code.get().memory[0]
>     itr: Union[ClassDocument, FunctionDocument, OPBlockDocument]
>     if (keyword.text == "class"):
>         itr = ClassDocument(
>             level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>             filedoc=self.FILEDOC,
>         )
>     elif (keyword.text == "def"):
>         itr = FunctionDocument(
>             level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>             filedoc=self.FILEDOC,
>         )
>     else:
>         itr = OPBlockDocument(
>             level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>             filedoc=self.FILEDOC,
>         )
>     self.components.append(itr)
>
>     # Parse code.
>     itr.parse(self.code)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainseriesdocument)

---

### Function: doc.main.SeriesDocument.dedent

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1088)

Check if a dedent is happening.

> **Arguments**
> - *self*: `SeriesDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   Signal of ending of a series. It is equivalent to dedent at the first next non-trival line.

> ```python
> # Move the pointer to next non-trival line.
> ptr = self.code.scan
> while (True):
>     # EOF is equivalent to dedent.
>     if (ptr == len(self.code.memory)):
>         return True
>     else:
>         pass
>
>     # Fetch line and check.
>     obj = self.code.memory[ptr]
>     if (len(obj.memory) == 1 and obj.memory[0].check(token.NL)):
>         pass
>     elif (obj.text == "# " + "=" * (MAX - 2)):
>         # Introduction is a  special stop signal for series.
>         return True
>     else:
>         break
>
>     # Move to next.
>     ptr += 1
> return self.code.memory[ptr].level < self.LEVEL
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainseriesdocument)

---

### Function: doc.main.SeriesDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1128)

Generate notes.

> **Arguments**
> - *self*: `SeriesDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Block notes is just a list of its statments notes.
> first = True
> for child in self.components:
>     # First item has no breaks.
>     if (first):
>         first = False
>     else:
>         self.markdown.append("")
>
>     # Generate child notes.
>     child.notes()
>     self.markdown.extend(child.markdown)
>
> # Clear children notes for memory efficency.
> for child in self.components:
>     child.markdown.clear()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainseriesdocument)

## Section: Class Code Document Objects

Code document for a definition of class. It can mutually import with SeriesDocument, thus it is put in this file.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.ClassDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1174)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a definition of class.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.ClassDocument.allocate](#function-docmainclassdocumentallocate)
  * [Function: doc.main.ClassDocument.parse](#function-docmainclassdocumentparse)
  * [Function: doc.main.ClassDocument.notes](#function-docmainclassdocumentnotes)
  * [Function: doc.main.ClassDocument.check\_inheritance](#function-docmainclassdocumentcheck_inheritance)

---

### Function: doc.main.ClassDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1178)

Allocate children memory.

> **Arguments**
> - *self*: `ClassDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Hierarchy of class body is limited and may change.
> if (self.HIERARCHY == GLOBAL):
>     hierarchy = CLASS
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " class is limited to be global level.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
>
> # Children are a description and a series of codes.
> self.description = ClassDescDocument(
>     level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
>     filedoc=self.FILEDOC,
> )
> self.body = SeriesDocument(
>     level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
>     filedoc=self.FILEDOC,
> )
>
> # Number of blank breaks is based on hierarchy.
> self.NUM_BLANKS = 1 + int(self.HIERARCHY == GLOBAL)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainclassdocument)

---

### Function: doc.main.ClassDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1216)

Parse information into document.

> **Arguments**
> - *self*: `ClassDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Get the class name.
> obj = self.code.get()
> obj.reset()
> obj.match("class", level=self.LEVEL)
> self.name = obj.get().text
> obj.match(token.NAME, level=self.LEVEL)
>
> # Get the super name.
> obj.match("(", level=self.LEVEL)
> buf = [obj.get().text]
> obj.match(token.NAME, level=self.LEVEL)
> while (obj.check(".", level=self.LEVEL)):
>     obj.match(".", level=self.LEVEL)
>     buf.append(obj.get().text)
>     obj.match(token.NAME, level=self.LEVEL)
> self.super = ".".join(buf)
> obj.match(")", level=self.LEVEL)
> obj.match(":", level=self.LEVEL)
> obj.match(token.NEWLINE, level=self.LEVEL)
> self.code.next()
>
> # Parse code.
> self.description.parse(self.code)
> self.body.parse(self.code)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainclassdocument)

---

### Function: doc.main.ClassDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1262)

Generate notes.

> **Arguments**
> - *self*: `ClassDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Get imported global variables sorted by inverse length.
> knowns = sorted(
>     getattr(self.FILEDOC.ROOTDOC, "classes").keys(),
>     key=lambda x: -len(x),
> )
>
> # Find the first variable matching the super name.
> for itr in knowns:
>     if (itr in self.super):
>         modname = self.FILEDOC.modules.mapping[itr]
>         dirpath = os.path.join(
>             self.FILEDOC.FOLDER, *modname.split(".")[:-1],
>         )
>         classname = self.super[len(modname) + 1:]
>         break
>     else:
>         modname = ""
>         dirpath = ""
>         classname = self.super
> if (len(modname) == 0 and classname in self.FILEDOC.classes):
>     modname = self.FILEDOC.ME
>     dirpath = self.FILEDOC.ROOTDOC.PATH
> else:
>     pass
>
> # Locate the super.
> if (len(modname) == 0):
>     # Python class has no reference.
>     link = self.super
> elif (dirpath == self.FILEDOC.ROOTDOC.PATH):
>     # Get in-page reference directly.
>     full = "{:s}.{:s}".format(modname, classname)
>     refer = "Class: {:s}".format(full)
>     refer = github_header(refer)
>     link = "[{:s}](#{:s})".format(full, refer)
> else:
>     # Get Github page.
>     print(dirpath, modname, classname)
>     raise NotImplementedError
>
> # Check inheritance.
> if (len(modname) > 0):
>     full = "{:s}.{:s}".format(modname, classname)
>     superdoc = getattr(self.FILEDOC.ROOTDOC, "classdocs")[full]
>     self.check_inheritance(
>         superdoc,
>         myname="{:s}.{:s}".format(self.FILEDOC.ME, self.name),
>         suname=full,
>     )
> else:
>     pass
>
> # Title is class name.
> self.markdown.extend(["---", ""])
> self.markdown.append("## Class: {:s}.{:s}".format(
>     self.FILEDOC.ME, self.name,
> ))
>
> # Super link to source code is required.
> source = os.path.join(
>     self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
> )
> source = "{:s}#L{:d}".format(source, self.row)
> self.markdown.append("")
> self.markdown.append("- Source: [Github]({:s})".format(source))
>
> # Super class is required.
> self.markdown.append("")
> self.markdown.append("- Super: {:s}".format(link))
>
> # Put descriptions here.
> for para in self.description.title:
>     self.markdown.append("")
>     self.markdown.append(" ".join(para))
>
> # Return to TOC, file.
> self.markdown.append("")
> self.markdown.append(
>     "[[TOC]](#table-of-content) [[File]](#{:s})".format(
>         github_header("File: {:s}".format(
>             self.FILEDOC.PATH,
>         )),
>     ),
> )
>
> # Get body note as a code block
> self.body.notes()
> buf = []
> for itr in self.body.markdown:
>     if (len(itr) == 0 or itr[0] != "#"):
>         buf.append(itr)
>     elif (itr[3] in ("F", "B")):
>         buf.append("#" + itr)
>     else:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " class can only documentize functions and blocks.",
>             self.FILEDOC.PATH, "line {:d}".format(self.row),
>         )
>         raise RuntimeError
> self.markdown.append("")
> self.markdown.append("- Members:")
> self.markdown.extend(toc(buf)[2:])
> self.markdown.append("")
> self.markdown.extend(buf)
>
> # Clear children notes for memory efficency.
> self.body.markdown.clear()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainclassdocument)

---

### Function: doc.main.ClassDocument.check\_inheritance

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1388)

Ensure inheritance.

> **Arguments**
> - *self*: `ClassDocument`
>
> - *superdoc*: `ClassDocument`
>
>   Document of super class.
>
> - *\*args*: `object`
>
> - *myname*: `str`
>
>   Focusing class name.
>
> - *suname*: `str`
>
>   Super class name.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Get functions of mine.
> self.myfuncs = {}
> for component in self.body.components:
>     if (isinstance(component, FunctionDocument)):
>         self.myfuncs[component.name] = component
>     else:
>         pass
>
> # Get functions of super.
> self.sufuncs = {}
> for component in superdoc.body.components:
>     if (isinstance(component, FunctionDocument)):
>         self.sufuncs[component.name] = component
>     else:
>         pass
>
> # Get override items.
> override = list(set(self.myfuncs.keys()) & set(self.sufuncs.keys()))
>
> # Get inheritance checking items.
> for itr in override:
>     func_consistency(
>         self.myfuncs[itr], su=self.sufuncs[itr], myname=myname,
>         suname=suname,
>     )
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainclassdocument)

---

## Function: doc.main.func\_consistency

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1438)

Ensure consistency.

> **Arguments**
> - *my*: `FunctionDocument`
>
>   Focusing class function document.
>
> - *\*args*: `object`
>
> - *su*: `FunctionDocument`
>
>   Super class function document.
>
> - *myname*: `str`
>
>   Focusing class name.
>
> - *suname*: `str`
>
>   Super class name.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Get esssential items.
> my_title = my.description.title
> my_arg_names = my.description.arg_names
> my_arg_descs = my.description.arg_descs
> my_ret_names = my.description.return_names
> my_ret_descs = my.description.return_descs
> my_attach = my.description.attach
> su_title = su.description.title
> su_arg_names = su.description.arg_names
> su_arg_descs = su.description.arg_descs
> su_ret_names = su.description.return_names
> su_ret_descs = su.description.return_descs
> su_attach = su.description.attach
>
> # Super texts should be a subset of my texts.
> if (is_subparagraphs(su_title, my_title)):
>     pass
> else:
>     error(
>         "Title text of \"{:s}.{:s}\" should a subset of" \
>         " \"{:s}.{:s}\".",
>         myname, my.name, suname, su.name,
>     )
>     raise RuntimeError
> if (is_subparagraphs(su_attach, my_attach)):
>     pass
> else:
>     error(
>         "Attached text of \"{:s}.{:s}\" should a subset of" \
>         " \"{:s}.{:s}\".",
>         myname, my.name, suname, su.name,
>     )
>     raise RuntimeError
>
> # Break ordered and keyword things.
> my_arg_break = order_key_argbreak(my_arg_names)
> su_arg_break = order_key_argbreak(su_arg_names)
> my_argord_names = my_arg_names[:my_arg_break - 1]
> my_argkey_names = my_arg_names[my_arg_break + 1:-1]
> my_argord_descs = my_arg_descs[:my_arg_break - 1]
> my_argkey_descs = my_arg_descs[my_arg_break + 1:-1]
> su_argord_names = su_arg_names[:my_arg_break - 1]
> su_argkey_names = su_arg_names[my_arg_break + 1:-1]
> su_argord_descs = su_arg_descs[:my_arg_break - 1]
> su_argkey_descs = su_arg_descs[my_arg_break + 1:-1]
>
> # Arguments and returns should also be subsets.
> if (is_subdefs(
>     su_argord_names, my_argord_names,
>     su_argord_descs, my_argord_descs,
> )):
>     pass
> else:
>     error(
>         "Ordered argument of \"{:s}.{:s}\" should a subset of" \
>         " \"{:s}.{:s}\".",
>         myname, my.name, suname, su.name,
>     )
>     raise RuntimeError
> if (is_subdefs(
>     su_argkey_names, my_argkey_names,
>     su_argkey_descs, my_argkey_descs,
> )):
>     pass
> else:
>     error(
>         "Keyword argument of \"{:s}.{:s}\" should a subset of" \
>         " \"{:s}.{:s}\".",
>         myname, my.name, suname, su.name,
>     )
>     raise RuntimeError
> if (is_subdefs(
>     su_ret_names, my_ret_names,
>     su_ret_descs, my_ret_descs,
> )):
>     pass
> else:
>     error(
>         "Return of \"{:s}.{:s}\" should a subset of" \
>         " \"{:s}.{:s}\".",
>         myname, my.name, suname, su.name,
>     )
>     raise RuntimeError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Function: doc.main.is\_subparagraphs

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1547)

Is a subset list of paragraphs.

> **Arguments**
> - *small*: `List[List[str]]`
>
>   Smaller paragraphs.
>
> - *large*: `List[List[str]]`
>
>   Larger paragraphs.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   If True, smaller one is subset of larger one.

> ```python
> # Check line by line.
> for i in range(len(small)):
>     if (i < len(large) and " ".join(small[i]) == " ".join(large[i])):
>         pass
>     else:
>         return False
> return True
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Function: doc.main.is\_subdefs

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1578)

Is a subset list of paragraphs.

> **Arguments**
> - *small1*: `List[str]`
>
>   Smaller names.
>
> - *large1*: `List[str]`
>
>   Larger names.
>
> - *small2*: `List[List[List[str]]]`
>
>   Smaller paragraphs.
>
> - *large2*: `List[List[List[str]]]`
>
>   Larger paragraphs.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   If True, smaller one is subset of larger one.

> ```python
> # Check name by name.
> for i in range(len(small1)):
>     if (i < len(large1) and small1[i] == large1[i]):
>         if (is_subparagraphs(small2[i], large2[i])):
>             pass
>         else:
>             return False
>     else:
>         return False
> return True
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Function: doc.main.order\_key\_argbreak

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1617)

Break position between ordered and keyword arguments

> **Arguments**
> - *names*: `List[str]`
>
>   Argument names.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *i*: `int`
>
>   Break index.

> ```python
> # Traverse to find.
> for i, itr in enumerate(names):
>     if (itr == "*args"):
>         return i
>     else:
>         pass
> return len(names)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

## Section: Function Code Document Objects

Code document for a definition of function. It can mutually import with SeriesDocument, thus it is put in this file.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.FunctionDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1656)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a definition of function.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.FunctionDocument.allocate](#function-docmainfunctiondocumentallocate)
  * [Function: doc.main.FunctionDocument.parse](#function-docmainfunctiondocumentparse)
  * [Function: doc.main.FunctionDocument.notes](#function-docmainfunctiondocumentnotes)

---

### Function: doc.main.FunctionDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1660)

Allocate children memory.

> **Arguments**
> - *self*: `FunctionDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Hierarchy of function body may change.
> if (self.HIERARCHY in (GLOBAL, CLASS)):
>     hierarchy = FUNCTION
> else:
>     hierarchy = self.HIERARCHY
>
> # Children are a description and a series of codes.
> self.description = FuncDescDocument(
>     level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
>     filedoc=self.FILEDOC,
> )
> self.body = SeriesDocument(
>     level=self.LEVEL + 1, hierarchy=hierarchy, superior=self,
>     filedoc=self.FILEDOC,
> )
>
> # Number of blank breaks is based on hierarchy.
> self.NUM_BLANKS = 1 + int(self.HIERARCHY == GLOBAL)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfunctiondocument)

---

### Function: doc.main.FunctionDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1695)

Parse information into document.

> **Arguments**
> - *self*: `FunctionDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Get the function name.
> obj = self.code.get()
> obj.reset()
> obj.match("def", level=self.LEVEL)
> self.name = obj.get().text
> obj.match(token.NAME, level=self.LEVEL)
>
> # Get the arguments.
> argdoc = ArgumentDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC, multiple=(obj.memory[-2].text != ":"),
> )
> argdoc.parse(self.code)
> obj = self.code.get()
> obj.match("->", level=self.LEVEL)
> returndoc = TypeHintDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC,
> )
> returndoc.parse(self.code)
> obj = self.code.get()
> obj.match(":", level=self.LEVEL)
> obj.match(token.NEWLINE, level=self.LEVEL)
> self.code.next()
>
> # Parse components.
> self.description.parse(self.code)
> self.description.review(argdoc, returndoc)
> self.body.parse(self.code)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfunctiondocument)

---

### Function: doc.main.FunctionDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1746)

Generate notes.

> **Arguments**
> - *self*: `FunctionDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # In deep level there is no need to provide details.
> if (self.HIERARCHY in (GLOBAL, CLASS)):
>     pass
> else:
>     self.markdown.append("def {:s}(...):".format(self.name))
>     self.markdown.append("{:s}...;".format(" " * UNIT))
>     return
>
> # Title is function name.
> self.markdown.extend(["---", ""])
> if (self.HIERARCHY == GLOBAL):
>     self.markdown.append("## Function: {:s}.{:s}".format(
>         self.FILEDOC.ME, self.name.replace("_", "\\_"),
>     ))
> else:
>     self.markdown.append("## Function: {:s}.{:s}.{:s}".format(
>         self.FILEDOC.ME, getattr(self.SUPERIOR.SUPERIOR, "name"),
>         self.name.replace("_", "\\_"),
>     ))
>
> # Super link to source code is required.
> source = os.path.join(
>     self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
> )
> source = "{:s}#L{:d}".format(source, self.row)
> self.markdown.append("")
> self.markdown.append("- Source: [Github]({:s})".format(source))
>
> # Add description 1 here.
> for para in self.description.title:
>     self.markdown.append("")
>     self.markdown.append(" ".join(para))
>
> # Add arguments.
> self.markdown.append("")
> self.markdown.append("> **Arguments**")
> ptr = 0
> while (ptr < len(self.description.arg_names)):
>     # The first argument has no breaks.
>     if (ptr == 0):
>         pass
>     else:
>         self.markdown.append(">")
>
>     # Get name and type hint first.
>     name = self.description.arg_names[ptr]
>     hint = self.description.arg_hints[ptr]
>     desc = self.description.arg_descs[ptr]
>     ptr += 1
>
>     # Some arguments have no attachment.
>     if (name == "*args"):
>         self.markdown.append("> - *{:s}*: `{:s}`".format(
>             "\\*args", hint,
>         ))
>     elif (name == "**kargs"):
>         self.markdown.append("> - *{:s}*: `{:s}`".format(
>             "\\*\\*kargs", hint,
>         ))
>     else:
>         self.markdown.append("> - *{:s}*: `{:s}`".format(name, hint))
>
>     # Output argument paragraphs with indent.
>     for para in desc:
>         self.markdown.append(">")
>         self.markdown.append(">   {:s}".format(" ".join(para)))
>
> # Add returns.
> self.markdown.append("")
> self.markdown.append("> **Returns**")
> ptr = 0
> while (ptr < len(self.description.return_names)):
>     # The first argument has no breaks.
>     if (ptr == 0):
>         pass
>     else:
>         self.markdown.append(">")
>
>     # Get name and type hint first.
>     name = self.description.return_names[ptr]
>     hint = self.description.return_hints[ptr]
>     desc = self.description.return_descs[ptr]
>     ptr += 1
>     self.markdown.append("> - *{:s}*: `{:s}`".format(name, hint))
>
>     # Output argument paragraphs with indent.
>     for para in desc:
>         self.markdown.append(">")
>         self.markdown.append(">   {:s}".format(" ".join(para)))
>
> # Add description 2 here.
> for para in self.description.attach:
>     self.markdown.append("")
>     self.markdown.append(" ".join(para))
>
> # Get body note as a code block
> self.body.notes()
> self.markdown.append("")
> self.markdown.append("> ```python")
> for itr in self.body.markdown:
>     if (len(itr) == 0):
>         self.markdown.append(">")
>     else:
>         self.markdown.append("> {:s}".format(itr))
> self.markdown.append("> ```")
>
> # Return to class.
> if (self.HIERARCHY == GLOBAL):
>     class_link = ""
> else:
>     holder = self.SUPERIOR.SUPERIOR
>     class_link = " [[Class]](#{:s})".format(
>         github_header("Class: {:s}.{:s}".format(
>             holder.FILEDOC.ME, getattr(holder, "name"),
>         )),
>     )
>
> # Return to TOC, file.
> self.markdown.append("")
> self.markdown.append(
>     "[[TOC]](#table-of-content) [[File]](#{:s}){:s}".format(
>         github_header("File: {:s}".format(
>             self.FILEDOC.PATH,
>         )),
>         class_link,
>     ),
> )
>
> # Clear children notes for memory efficency.
> self.body.markdown.clear()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfunctiondocument)

## Section: Operation Block Code Document Objects

Code document for a block of operation code. It can mutually import with SeriesDocument, thus it is put in this file.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.OPBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1906)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a block of operation code.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Block: doc.main.OPBlockDocument: Define constants.](#block-docmainopblockdocument-define-constants)
  * [Function: doc.main.OPBlockDocument.allocate](#function-docmainopblockdocumentallocate)
  * [Function: doc.main.OPBlockDocument.parse](#function-docmainopblockdocumentparse)
  * [Function: doc.main.OPBlockDocument.notes](#function-docmainopblockdocumentnotes)

---

### Block: doc.main.OPBlockDocument: Define constants.

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1910)

> ```python
> # Define constants.
> MAX = 20
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainopblockdocument)

---

### Function: doc.main.OPBlockDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1913)

Allocate children memory.

> **Arguments**
> - *self*: `OPBlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Children are a description and a block of operations.
> self.comment = CommentDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC,
> )
>
> # Number of blank breaks is based on hierarchy.
> self.NUM_BLANKS = 1 + int(self.HIERARCHY == GLOBAL)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainopblockdocument)

---

### Function: doc.main.OPBlockDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1938)

Parse information into document.

> **Arguments**
> - *self*: `OPBlockDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Parse comment code.
> self.comment.parse(self.code)
> self.memory = []
> while (True):
>     if (self.code.eof() or self.code.blank_top(self.NUM_BLANKS)):
>         break
>     else:
>         self.memory.append(self.code.get())
>         self.code.next()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainopblockdocument)

---

### Function: doc.main.OPBlockDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L1969)

Generate notes.

> **Arguments**
> - *self*: `OPBlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Get code snap with comments.
> snap = []
> self.comment.notes()
> snap.extend(self.comment.markdown)
> start = self.LEVEL * UNIT
> for com in self.memory:
>     snap.append(com.text[start:])
>
> # Clear children notes for memory efficency.
> self.comment.markdown.clear()
>
> # In deep level there is no need to wrap headers.
> if (self.HIERARCHY in (GLOBAL, CLASS)):
>     pass
> else:
>     self.markdown.extend(snap)
>     return
>
> # Get first sentence in the comment with limited length.
> title = self.comment.paragraphs[0][0]
> if (len(title) > self.MAX):
>     title = title[0:self.MAX - 3].strip() + "..."
> else:
>     pass
> self.markdown.extend(["---", ""])
> if (self.HIERARCHY == GLOBAL):
>     self.markdown.append("## Block: {:s}: {:s}".format(
>         self.FILEDOC.ME, title,
>     ))
> else:
>     self.markdown.append("## Block: {:s}.{:s}: {:s}".format(
>         self.FILEDOC.ME, getattr(self.SUPERIOR.SUPERIOR, "name"),
>         title,
>     ))
>
> # Super link to source code is required.
> source = os.path.join(
>     self.FILEDOC.GITHUB, "blob", "master", self.FILEDOC.PATH,
> )
> source = "{:s}#L{:d}".format(source, self.row)
> self.markdown.append("")
> self.markdown.append("- Source: [Github]({:s})".format(source))
>
> # Add code snap here.
> self.markdown.append("")
> self.markdown.append("> ```python")
> for itr in snap:
>     if (len(itr) == 0):
>         self.markdown.append(">")
>     else:
>         self.markdown.append("> {:s}".format(itr))
> self.markdown.append("> ```")
>
> # Return to class.
> if (self.HIERARCHY == GLOBAL):
>     class_link = ""
> else:
>     holder = self.SUPERIOR.SUPERIOR
>     class_link = " [[Class]](#{:s})".format(
>         github_header("Class: {:s}.{:s}".format(
>             holder.FILEDOC.ME, getattr(holder, "name"),
>         )),
>     )
>
> # Return to TOC, file.
> self.markdown.append("")
> self.markdown.append(
>     "[[TOC]](#table-of-content) [[File]](#{:s}){:s}".format(
>         github_header("File: {:s}".format(
>             self.FILEDOC.PATH,
>         )),
>         class_link,
>     ),
> )
>
> # Clear children notes for memory efficency.
> pass
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainopblockdocument)

## Section: Function Code Document Objects

Code document for function related codes. This only contains elements of a function, for example, arguments, returns. The function document itself is defined in series module.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.TypeHintDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2077)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for type hint definition.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.TypeHintDocument.allocate](#function-docmaintypehintdocumentallocate)
  * [Function: doc.main.TypeHintDocument.parse](#function-docmaintypehintdocumentparse)
  * [Function: doc.main.TypeHintDocument.parse\_type](#function-docmaintypehintdocumentparse_type)
  * [Function: doc.main.TypeHintDocument.text](#function-docmaintypehintdocumenttext)

---

### Function: doc.main.TypeHintDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2081)

Allocate children memory.

> **Arguments**
> - *self*: `TypeHintDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Allocate children hints.
> self.children: List[TypeHintDocument] = []
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaintypehintdocument)

---

### Function: doc.main.TypeHintDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2100)

Parse information into document.

> **Arguments**
> - *self*: `TypeHintDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Get type name.
> obj = self.code.get()
> self.name = self.parse_type(obj)
>
> # Get children type hint if it exists.
> if (obj.check("[", level=self.LEVEL)):
>     pass
> else:
>     return
>
> # Match left.
> obj.match("[", level=self.LEVEL)
> if (obj.check(token.NL, level=self.LEVEL)):
>     multiple = True
>     obj.match(token.NL, level=self.LEVEL)
>     self.code.next()
>     obj = self.code.get()
>     obj.reset()
> else:
>     multiple = False
>
> # Deal with recursive hints.
> level2 = self.LEVEL + int(multiple)
> while (not self.code.eof()):
>     # Right means ending.
>     if (obj.check("]", level=self.LEVEL)):
>         break
>     else:
>         pass
>
>     # Get type hint.
>     hint = TypeHintDocument(
>         level=level2, hierarchy=self.HIERARCHY, superior=self,
>         filedoc=self.FILEDOC,
>     )
>     hint.parse(self.code)
>     self.children.append(hint)
>
>     # Get break.
>     if (obj.check("]", level=self.LEVEL)):
>         break
>     else:
>         obj.match(",", level=level2)
>
>     # May reach the end of a line.
>     if (obj.check(token.NL, level=level2)):
>         obj.match(token.NL, level=level2)
>         self.code.next()
>         obj = self.code.get()
>         obj.reset()
>     else:
>         pass
>
> # Match right.
> obj.match("]", level=self.LEVEL)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaintypehintdocument)

---

### Function: doc.main.TypeHintDocument.parse\_type

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2177)

Parse information (type) into document.

> **Arguments**
> - *self*: `TypeHintDocument`
>
> - *line*: `Line`
>
>   A line of parsing code words.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *name*: `str`
>
>   Type name.

> ```python
> # Module is a list of names concatenated by ".".
> buf = [line.get().text]
> line.match(token.NAME, level=self.LEVEL)
> while (line.check(".", level=self.LEVEL)):
>     line.match(".", level=self.LEVEL)
>     buf.append(line.get().text)
>     line.match(token.NAME, level=self.LEVEL)
> return ".".join(buf)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaintypehintdocument)

---

### Function: doc.main.TypeHintDocument.text

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2206)

Get text message of type hint.

> **Arguments**
> - *self*: `TypeHintDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *msg*: `str`
>
>   Message.

> ```python
> # Get name recursively.
> if (len(self.children) > 0):
>     buf = [itr.text() for itr in self.children]
>     recursive = "[{:s}]".format(", ".join(buf))
> else:
>     recursive = ""
> return "{:s}{:s}".format(self.name, recursive)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaintypehintdocument)

---

## Class: doc.main.ArgumentDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2231)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for argument definition.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.ArgumentDocument.\_\_init\_\_](#function-docmainargumentdocument__init__)
  * [Function: doc.main.ArgumentDocument.allocate](#function-docmainargumentdocumentallocate)
  * [Function: doc.main.ArgumentDocument.parse](#function-docmainargumentdocumentparse)

---

### Function: doc.main.ArgumentDocument.\_\_init\_\_

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2235)

Initialize.

> **Arguments**
> - *self*: `ArgumentDocument`
>
> - *\*args*: `object`
>
> - *level*: `int`
>
>   Indent level.
>
> - *hierarchy*: `int`
>
>   Hierarchy integer.
>
> - *superior*: `Union[CodeDocument, None]`
>
>   Superior code document.
>
> - *filedoc*: `FileDocument`
>
>   Document of the file of the code.
>
> - *multiple*: `bool`
>
>   If True, argument is multiple-line definition.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.__init__(
>     self, *args, level=level, hierarchy=hierarchy, superior=superior,
>     filedoc=filedoc, **kargs,
> )
>
> # Save necessary attributes.
> self.MULTIPLE = multiple
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainargumentdocument)

---

### Function: doc.main.ArgumentDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2273)

Allocate children memory.

> **Arguments**
> - *self*: `ArgumentDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Allocate argument buffer.
> self.items: List[Tuple[str, TypeHintDocument]] = []
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainargumentdocument)

---

### Function: doc.main.ArgumentDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2292)

Parse information into document.

> **Arguments**
> - *self*: `ArgumentDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Match left.
> obj = self.code.get()
> obj.match("(", level=self.LEVEL)
> if (self.MULTIPLE):
>     obj.match(token.NL, level=self.LEVEL)
>     self.code.next()
>     obj = self.code.get()
>     obj.reset()
> else:
>     pass
>
> # Match argument names and type hints.
> level2 = self.LEVEL + int(self.MULTIPLE)
> while (not self.code.eof()):
>     # Right means ending.
>     if (obj.check(")", level=self.LEVEL)):
>         break
>     else:
>         pass
>
>     # It is possible to have "*args" and "**kargs".
>     if (obj.check("*", level=level2)):
>         prefix = "*"
>         obj.match("*", level=level2)
>     elif (obj.check("**", level=level2)):
>         prefix = "**"
>         obj.match("**", level=level2)
>     else:
>         prefix = ""
>
>     # Get argument name.
>     suffix = obj.get().text
>     obj.match(token.NAME, level=level2)
>     name = prefix + suffix
>
>     # Get type hint.
>     obj.match(":", level=level2)
>     hint = TypeHintDocument(
>         level=level2, hierarchy=self.HIERARCHY, superior=self,
>         filedoc=self.FILEDOC,
>     )
>     hint.parse(self.code)
>     self.items.append((name, hint))
>
>     # Get break.
>     if (obj.check(")", level=self.LEVEL)):
>         break
>     else:
>         obj.match(",", level=level2)
>
>     # May reach the end of a line.
>     if (obj.check(token.NL, level=level2)):
>         obj.match(token.NL, level=level2)
>         self.code.next()
>         obj = self.code.get()
>         obj.reset()
>     else:
>         pass
>
> # Match right.
> obj.match(")", level=self.LEVEL)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainargumentdocument)

## Section: Block Code Document Objects

Code document on block level. There are several kinds of block documents, but they all share the same workflow.

A block often start with several comments lines, except that in a branch with only one block, it may have no comments.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.BlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2391)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a block of code prototype.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.BlockDocument.allocate](#function-docmainblockdocumentallocate)
  * [Function: doc.main.BlockDocument.allocate\_statements](#function-docmainblockdocumentallocate_statements)
  * [Function: doc.main.BlockDocument.parse](#function-docmainblockdocumentparse)
  * [Function: doc.main.BlockDocument.parse\_statements](#function-docmainblockdocumentparse_statements)

---

### Function: doc.main.BlockDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2395)

Allocate children memory.

> **Arguments**
> - *self*: `BlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Block ususally start with a comment, then statements.
> self.comment = CommentDocument(
>     level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>     filedoc=self.FILEDOC,
> )
> self.allocate_statements()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainblockdocument)

---

### Function: doc.main.BlockDocument.allocate\_statements

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2418)

Allocate statement children memory.

> **Arguments**
> - *self*: `BlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Prototype may not implement everything.
> error("Function is not implemented.")
> raise NotImplementedError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainblockdocument)

---

### Function: doc.main.BlockDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2438)

Parse information into document.

> **Arguments**
> - *self*: `BlockDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Parse code.
> self.comment.parse(self.code)
> self.parse_statements()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainblockdocument)

---

### Function: doc.main.BlockDocument.parse\_statements

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2463)

Parse all statements of the document.

> **Arguments**
> - *self*: `BlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Prototype may not implement everything.
> error("Function is not implemented.")
> raise NotImplementedError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainblockdocument)

---

## Class: doc.main.ImportBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2484)

- Super: [doc.main.BlockDocument](#class-docmainblockdocument)

Document for a block of import code.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.ImportBlockDocument.allocate\_statements](#function-docmainimportblockdocumentallocate_statements)
  * [Function: doc.main.ImportBlockDocument.parse\_statements](#function-docmainimportblockdocumentparse_statements)
  * [Function: doc.main.ImportBlockDocument.eob](#function-docmainimportblockdocumenteob)
  * [Function: doc.main.ImportBlockDocument.notes](#function-docmainimportblockdocumentnotes)
  * [Function: doc.main.ImportBlockDocument.check](#function-docmainimportblockdocumentcheck)

---

### Function: doc.main.ImportBlockDocument.allocate\_statements

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2488)

Allocate statement children memory.

> **Arguments**
> - *self*: `ImportBlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Import block only has import statements.
> self.statements: List[ImportDocument] = []
>
> # Save imported modules.
> self.modules: Dict[str, List[str]] = {}
> self.identifiers: Dict[str, str] = {}
> self.mapping: Dict[str, str] = {}
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportblockdocument)

---

### Function: doc.main.ImportBlockDocument.parse\_statements

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2512)

Parse all statements of the document.

> **Arguments**
> - *self*: `ImportBlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Parsea a new document from current line.
> while (not self.eob()):
>     child = ImportDocument(
>         level=self.LEVEL, hierarchy=self.HIERARCHY, superior=self,
>         filedoc=self.FILEDOC,
>     )
>     child.parse(self.code)
>     self.statements.append(child)
>     self.code.next()
>
> # Merge all imports.
> for child in self.statements:
>     for name, members in child.modules.items():
>         if (name in self.modules):
>             pass
>         else:
>             self.modules[name] = []
>         self.modules[name].extend(members)
>     for name, source in child.identifiers.items():
>         self.identifiers[name] = source
>     for rename, name in child.mapping.items():
>         self.mapping[rename] = name
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportblockdocument)

---

### Function: doc.main.ImportBlockDocument.eob

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2551)

Check end of the block.

> **Arguments**
> - *self*: `ImportBlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   Signal for end of the block.

> ```python
> # A single blank line is the end.
> return self.code.blank_top(1)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportblockdocument)

---

### Function: doc.main.ImportBlockDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2570)

Generate notes.

> **Arguments**
> - *self*: `ImportBlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Block notes is just a list of its statments notes.
> self.comment.notes()
> self.markdown.extend(self.comment.markdown)
> for itr in self.statements:
>     itr.notes()
>     self.markdown.extend(itr.markdown)
>
> # Clear children notes for memory efficency.
> self.comment.markdown.clear()
> for itr in self.statements:
>     itr.markdown.clear()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportblockdocument)

---

### Function: doc.main.ImportBlockDocument.check

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2601)

Check if requiring row is exactly the given text.

> **Arguments**
> - *self*: `ImportBlockDocument`
>
> - *i*: `int`
>
>   Row ID.
>
> - *text*: `str`
>
>   Requiring text.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   If the text is satisfied.

This is specially defined because some imports are constantly required.

> ```python
> # Match directly
> return self.statements[i].memory.text == text
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportblockdocument)

---

## Class: doc.main.ConstBlockDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2629)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a block of constant code.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.ConstBlockDocument.\_\_init\_\_](#function-docmainconstblockdocument__init__)
  * [Function: doc.main.ConstBlockDocument.allocate](#function-docmainconstblockdocumentallocate)
  * [Function: doc.main.ConstBlockDocument.parse](#function-docmainconstblockdocumentparse)
  * [Function: doc.main.ConstBlockDocument.notes](#function-docmainconstblockdocumentnotes)

---

### Function: doc.main.ConstBlockDocument.\_\_init\_\_

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2633)

Initialize.

> **Arguments**
> - *self*: `ConstBlockDocument`
>
> - *\*args*: `object`
>
> - *level*: `int`
>
>   Indent level.
>
> - *hierarchy*: `int`
>
>   Hierarchy integer.
>
> - *superior*: `Union[CodeDocument, None]`
>
>   Superior code document.
>
> - *filedoc*: `FileDocument`
>
>   Document of the file of the code.
>
> - *constant*: `str`
>
>   Constant code text.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.__init__(
>     self, *args, level=level, hierarchy=hierarchy, superior=superior,
>     filedoc=filedoc, **kargs,
> )
>
> # Save necessary attributes.
> self.CONSTANT = constant.split("\n")
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainconstblockdocument)

---

### Function: doc.main.ConstBlockDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2671)

Allocate children memory.

> **Arguments**
> - *self*: `ConstBlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Allocate document memory for constant lines.
> self.memory: List[Line] = []
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainconstblockdocument)

---

### Function: doc.main.ConstBlockDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2690)

Parse information into document.

> **Arguments**
> - *self*: `ConstBlockDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Get current line.
> for i, itr in enumerate(self.CONSTANT):
>     # Get current line.
>     obj = self.code.get()
>
>     # Directly match the constant text with current line.
>     if (obj.text == itr):
>         pass
>     else:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " expect\n\"\"\"\n{:s}\n\"\"\", but" \
>             " get\n\"\"\"\n{:s}\"\"\".",
>             self.FILEDOC.PATH, "line {:d}".format(obj.row),
>             itr, obj.text,
>         )
>         raise RuntimeError
>
>     # Save verified line in document memory.
>     self.memory.append(obj)
>     self.code.next()
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainconstblockdocument)

---

### Function: doc.main.ConstBlockDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2733)

Generate notes.

> **Arguments**
> - *self*: `ConstBlockDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Block notes is just a list of code lines without indents.
> start = self.LEVEL * UNIT
> for itr in self.memory:
>     self.markdown.append(itr.text[start:])
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainconstblockdocument)

## Section: Statement Code Document Objects

Code document for a line of statement. Different statement types have their own workflow, but they all save line of tokens belong to them for potential styled code recovery.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Class: doc.main.CommentDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2770)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a line of comment statement.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.CommentDocument.allocate](#function-docmaincommentdocumentallocate)
  * [Function: doc.main.CommentDocument.parse](#function-docmaincommentdocumentparse)
  * [Function: doc.main.CommentDocument.translate](#function-docmaincommentdocumenttranslate)
  * [Function: doc.main.CommentDocument.notes](#function-docmaincommentdocumentnotes)

---

### Function: doc.main.CommentDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2774)

Allocate children memory.

> **Arguments**
> - *self*: `CommentDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Allocate document memory for comment lines.
> self.memory: List[Line] = []
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaincommentdocument)

---

### Function: doc.main.CommentDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2793)

Parse information into document.

> **Arguments**
> - *self*: `CommentDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Read in all consecutive comments.
> texts = []
> while (not self.code.eof()):
>     # Get current line.
>     obj = self.code.get()
>     obj.reset()
>
>     # Stop for non-comment token head.
>     if (obj.check(token.COMMENT, level=self.LEVEL)):
>         pass
>     else:
>         break
>
>     # Parse current line.
>     comment = obj.get().text
>     obj.match(token.COMMENT, level=self.LEVEL)
>     obj.match(token.NL, level=self.LEVEL)
>     texts.append(comment[2:])
>
>     # Save and move to next line.
>     self.memory.append(obj)
>     self.code.next()
>
> # Translate parsed text into paragraphs.
> self.translate(texts)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaincommentdocument)

---

### Function: doc.main.CommentDocument.translate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2840)

Translate parsed text into paragraphs.

> **Arguments**
> - *self*: `CommentDocument`
>
> - *texts*: `List[str]`
>
>   A list of parsed comment texts.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Translate parsed text into paragraphs.
> try:
>     self.paragraphs = paragraphize(texts)
> except:
>     # Extend paragraph error report.
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " fail to translate paragraphs.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaincommentdocument)

---

### Function: doc.main.CommentDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2871)

Generate notes.

> **Arguments**
> - *self*: `CommentDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Statement note is just its code lines without indents.
> start = self.LEVEL * UNIT
> for itr in self.memory:
>     self.markdown.append(itr.text[start:])
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaincommentdocument)

---

## Class: doc.main.ImportDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2894)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a line of import statement.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.ImportDocument.allocate](#function-docmainimportdocumentallocate)
  * [Function: doc.main.ImportDocument.parse](#function-docmainimportdocumentparse)
  * [Function: doc.main.ImportDocument.parse\_import](#function-docmainimportdocumentparse_import)
  * [Function: doc.main.ImportDocument.parse\_from](#function-docmainimportdocumentparse_from)
  * [Function: doc.main.ImportDocument.parse\_module](#function-docmainimportdocumentparse_module)
  * [Function: doc.main.ImportDocument.parse\_identifier](#function-docmainimportdocumentparse_identifier)
  * [Function: doc.main.ImportDocument.parse\_rename](#function-docmainimportdocumentparse_rename)
  * [Function: doc.main.ImportDocument.append\_module](#function-docmainimportdocumentappend_module)
  * [Function: doc.main.ImportDocument.append\_identifier](#function-docmainimportdocumentappend_identifier)
  * [Function: doc.main.ImportDocument.notes](#function-docmainimportdocumentnotes)

---

### Function: doc.main.ImportDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2898)

Allocate children memory.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Save imported modules.
> self.modules: Dict[str, List[str]] = {}
> self.identifiers: Dict[str, str] = {}
> self.mapping: Dict[str, str] = {}
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2917)

Parse information into document.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Get current line and parse according to the first word.
> obj = self.code.get()
> obj.reset()
> getattr(self, "parse_{:s}".format(obj.get().text))(obj)
>
> # Save the only parsed line in document memory.
> self.memory = obj
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.parse\_import

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2946)

Parse information (import, as) into document.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *line*: `Line`
>
>   A line of parsing code words.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # First word is fixed.
> self.type = "import"
> line.match("import", level=self.LEVEL)
>
> # Match the module name.
> module = self.parse_module(line)
> rename = self.parse_rename(line)
> self.append_module(module, rename)
> line.match(token.NEWLINE, level=self.LEVEL)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.parse\_from

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L2974)

Parse information (from, import, as) into document.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *line*: `Line`
>
>   A line of parsing code words.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # First word is fixed.
> self.type = "from"
> line.match("from", level=self.LEVEL)
>
> # Match the module name.
> module = self.parse_module(line)
>
> # Next word is fixed.
> line.match("import", level=self.LEVEL)
>
> # Match identifiers until the end of the line.
> first = True
> while (not line.eol()):
>     if (first):
>         first = False
>     elif (line.check(",", level=self.LEVEL)):
>         line.match(",", level=self.LEVEL)
>     else:
>         break
>     identifier = self.parse_identifier(line)
>     rename = self.parse_rename(line)
>     self.append_identifier(identifier, rename, module=module)
> line.match(token.NEWLINE, level=self.LEVEL)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.parse\_module

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3016)

Parse information (module) into document.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *line*: `Line`
>
>   A line of parsing code words.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *name*: `str`
>
>   Module name.

> ```python
> # Module is a list of names concatenated by ".".
> buf = [line.get().text]
> line.match(token.NAME, level=self.LEVEL)
> while (line.check(".", level=self.LEVEL)):
>     line.match(".", level=self.LEVEL)
>     buf.append(line.get().text)
>     line.match(token.NAME, level=self.LEVEL)
> return ".".join(buf)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.parse\_identifier

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3045)

Parse information (identifier) into document.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *line*: `Line`
>
>   A line of parsing code words.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *name*: `str`
>
>   Identifier name.

> ```python
> # Identifier is just a name.
> name = line.get().text
> line.match(token.NAME, level=self.LEVEL)
> return name
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.parse\_rename

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3070)

Parse information (as) into document.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *line*: `Line`
>
>   A line of parsing code words.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *name*: `Union[str, None]`
>
>   Identifier name.

> ```python
> # First word is fixed or rename is not defined.
> if (line.check("as", level=self.LEVEL)):
>     line.match("as", level=self.LEVEL)
> else:
>     return None
>
> # Rename is just a name.
> name = line.get().text
> line.match(token.NAME, level=self.LEVEL)
> return name
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.append\_module

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3101)

Append an identifier import to document.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *module*: `str`
>
>   Module name.
>
> - *module2*: `Union[str, None]`
>
>   Module rename.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

Trace module and identifier name mappings. There final name should be unique in the file since both are globally claimed. If collision happens, overwrite as python does.

> ```python
> # Trace rename of the module.
> self.modules[module] = []
> if (module2 is None):
>     self.mapping[module] = module
> else:
>     self.mapping[module2] = module
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.append\_identifier

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3133)

Append an identifier import to document.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *identifier*: `str`
>
>   Identifier name.
>
> - *identifier2*: `Union[str, None]`
>
>   Identifier rename.
>
> - *\*args*: `object`
>
> - *module*: `str`
>
>   Module name.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Import module first if it has not been imported.
> if (module in self.modules):
>     pass
> else:
>     self.modules[module] = []
>
> # Trace module and rename of the identifier.
> if (identifier2 is None):
>     self.identifiers[identifier] = module
> else:
>     self.identifiers[identifier2] = module
> if (identifier2 is None):
>     self.mapping[identifier] = identifier
> else:
>     self.mapping[identifier2] = identifier
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

### Function: doc.main.ImportDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3172)

Generate notes.

> **Arguments**
> - *self*: `ImportDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Statement note is just its code lines without indents.
> start = self.LEVEL * UNIT
> self.markdown.append(self.memory.text[start:])
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainimportdocument)

---

## Class: doc.main.IntroDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3194)

- Super: [doc.main.CommentDocument](#class-docmaincommentdocument)

Document for an introduction statement.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.IntroDocument.translate](#function-docmainintrodocumenttranslate)
  * [Function: doc.main.IntroDocument.notes](#function-docmainintrodocumentnotes)

---

### Function: doc.main.IntroDocument.translate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3198)

Translate parsed text into paragraphs.

> **Arguments**
> - *self*: `IntroDocument`
>
> - *texts*: `List[str]`
>
>   A list of parsed introduction texts.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Head and tail are constant.
> if (
>     texts[0] == "=" * (MAX - 2) and
>     texts[1] == "*" * (MAX - 2) and
>     texts[2] == "-" * (MAX - 2) and
>     texts[-3] == "-" * (MAX - 2) and
>     texts[-2] == "*" * (MAX - 2) and
>     texts[-1] == "=" * (MAX - 2) and
>     texts[3][0:3] == "<< " and texts[3][-3:] == " >>"
> ):
>     pass
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " introduction requires constant head and tail lines.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
>
> # The first line must be the only title.
> words = texts[3][3:-3].split(" ")
> for itr in words:
>     if (re.match(FIRST, itr) is None):
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " introduction requires title words to be capitalized.",
>             self.FILEDOC.PATH, "line {:d}".format(self.row),
>         )
>         raise RuntimeError
>     else:
>         pass
> self.title = " ".join(words)
>
> # Translate parsed text into paragraphs.
> try:
>     self.paragraphs = paragraphize(texts[4:-3])
> except:
>     # Extend paragraph error report.
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " fail to translate paragraphs.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainintrodocument)

---

### Function: doc.main.IntroDocument.notes

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3261)

Generate notes.

> **Arguments**
> - *self*: `IntroDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

This will generate notes for console and markdown in the same time. For most part of the notes, they will share the same Markdown syntex except that console notes will use ASCII color codes for some keywords.

> ```python
> # Statement note is just its code lines without indents.
> self.markdown.append("## Section: {:s}".format(self.title))
> for itr in self.paragraphs:
>     self.markdown.append("")
>     self.markdown.append(" ".join(itr))
>
> # Return to TOC, file.
> self.markdown.append("")
> self.markdown.append(
>     "[[TOC]](#table-of-content) [[File]](#{:s})".format(
>         github_header("File: {:s}".format(
>             self.FILEDOC.PATH,
>         )),
>     ),
> )
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainintrodocument)

---

## Class: doc.main.DescriptionDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3295)

- Super: [doc.main.CodeDocument](#class-docmaincodedocument)

Document for a description statement prototype.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.DescriptionDocument.allocate](#function-docmaindescriptiondocumentallocate)
  * [Function: doc.main.DescriptionDocument.parse](#function-docmaindescriptiondocumentparse)
  * [Function: doc.main.DescriptionDocument.decode](#function-docmaindescriptiondocumentdecode)

---

### Function: doc.main.DescriptionDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3299)

Allocate children memory.

> **Arguments**
> - *self*: `DescriptionDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Allocate document memory for comment lines.
> self.memory: List[Line] = []
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindescriptiondocument)

---

### Function: doc.main.DescriptionDocument.parse

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3318)

Parse information into document.

> **Arguments**
> - *self*: `DescriptionDocument`
>
> - *code*: `Code`
>
>   Code scanner used for parsing.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> CodeDocument.parse(self, code, *args, **kargs)
>
> # Get description.
> obj = self.code.get()
> obj.reset()
> text = obj.get().text
> obj.match(token.STRING, level=self.LEVEL)
>
> # Description always occupy multiple lines.
> while (True):
>     if (obj.eol()):
>         self.memory.append(obj)
>         self.code.next()
>         obj = self.code.get()
>         obj.reset()
>     elif (obj.check(token.NEWLINE, level=self.LEVEL)):
>         break
>     else:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " description should occupy multiple lines without" \
>             " anything else.",
>             self.FILEDOC.PATH, "line {:d}".format(self.row),
>         )
>         raise RuntimeError
> obj.match(token.NEWLINE, level=self.LEVEL)
> self.memory.append(obj)
> self.code.next()
>
> # Remove indent from description.
> decoding = text.split("\n")
> for i in range(1, len(decoding)):
>     if (len(decoding[i]) > 0):
>         decoding[i] = decoding[i][UNIT * self.LEVEL:]
>     else:
>         pass
>
> # Description has content head and tail.
> if (decoding[0] == "r\"\"\"" and decoding[-1] == "\"\"\""):
>     pass
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " description has constant head and tail",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
>
> # Decode description.
> self.decode(decoding[1:-1])
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindescriptiondocument)

---

### Function: doc.main.DescriptionDocument.decode

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3388)

Decode list of texts into document.

> **Arguments**
> - *self*: `DescriptionDocument`
>
> - *texts*: `List[str]`
>
>   A list of decoding texts.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Prototype may not implement everything.
> error("Function is not implemented.")
> raise NotImplementedError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmaindescriptiondocument)

---

## Class: doc.main.ClassDescDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3412)

- Super: [doc.main.DescriptionDocument](#class-docmaindescriptiondocument)

Document for a description of class statement.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.ClassDescDocument.allocate](#function-docmainclassdescdocumentallocate)
  * [Function: doc.main.ClassDescDocument.decode](#function-docmainclassdescdocumentdecode)

---

### Function: doc.main.ClassDescDocument.allocate

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3416)

Allocate children memory.

> **Arguments**
> - *self*: `ClassDescDocument`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Super.
> DescriptionDocument.allocate(self, *args, **kargs)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainclassdescdocument)

---

### Function: doc.main.ClassDescDocument.decode

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3435)

Decode list of texts into document.

> **Arguments**
> - *self*: `ClassDescDocument`
>
> - *texts*: `List[str]`
>
>   A list of decoding texts.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Translate parsed text into paragraphs.
> try:
>     self.title = paragraphize(texts)
> except:
>     # Extend paragraph error report.
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " fail to translate paragraphs.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainclassdescdocument)

---

## Class: doc.main.FuncDescDocument

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3467)

- Super: [doc.main.DescriptionDocument](#class-docmaindescriptiondocument)

Document for a description of function statement.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

- Members:
  * [Function: doc.main.FuncDescDocument.decode](#function-docmainfuncdescdocumentdecode)
  * [Function: doc.main.FuncDescDocument.review](#function-docmainfuncdescdocumentreview)
  * [Function: doc.main.FuncDescDocument.review\_args](#function-docmainfuncdescdocumentreview_args)
  * [Function: doc.main.FuncDescDocument.review\_returns](#function-docmainfuncdescdocumentreview_returns)

---

### Function: doc.main.FuncDescDocument.decode

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3471)

Decode list of texts into document.

> **Arguments**
> - *self*: `FuncDescDocument`
>
> - *texts*: `List[str]`
>
>   A list of decoding texts.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Split into 4 parts by the first 3 blank lines.
> ptr = 0
> breaks = [0, 0, 0]
> for i in range(len(texts)):
>     if (len(texts[i]) == 0):
>         breaks[ptr] = i
>         ptr += 1
>         if (ptr == len(breaks)):
>             break
>         else:
>             pass
>     else:
>         pass
> texts_1 = texts[0:breaks[0]]
> texts_args = texts[breaks[0] + 1:breaks[1]]
> texts_returns = texts[breaks[1] + 1:breaks[2]]
> texts_2 = texts[breaks[2] + 1:]
>
> # Translate parsed text into paragraphs.
> try:
>     self.title = paragraphize(texts_1)
> except:
>     # Extend paragraph error report.
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " fail to translate paragraphs.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
>
> # Translate parsed text into paragraphs.
> try:
>     self.attach = paragraphize(texts_2)
> except:
>     # Extend paragraph error report.
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " fail to translate paragraphs.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
>
> # Save argument and return description for later review.
> self.texts_args = texts_args
> self.texts_returns = texts_returns
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfuncdescdocument)

---

### Function: doc.main.FuncDescDocument.review

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3536)

Review argument and return.

> **Arguments**
> - *self*: `FuncDescDocument`
>
> - *argdoc*: `ArgumentDocument`
>
>   Argument document.
>
> - *returndoc*: `TypeHintDocument`
>
>   Return document.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Review separately.
> self.review_args(argdoc)
> self.review_returns(returndoc)
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfuncdescdocument)

---

### Function: doc.main.FuncDescDocument.review\_args

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3561)

Review argument and return.

> **Arguments**
> - *self*: `FuncDescDocument`
>
> - *argdoc*: `ArgumentDocument`
>
>   Argument document.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Get texts.
> texts = self.texts_args
>
> # Argument description has constant head.
> if (texts[0] == "Args" and texts[1] == "----"):
>     pass
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " argument document has constant head.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
>
> # Traverse later contents.
> ptr = 0
> texts = texts[2:]
> num = 0
> self.arg_names = []
> self.arg_hints = []
> self.arg_descs: List[List[List[str]]] = []
> while (ptr < len(texts)):
>     # Get argument name.
>     name = texts[ptr][2:]
>     ptr += 1
>
>     # Get definition.
>     if (num == len(argdoc.items)):
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " defined arguments are less than described arguments.",
>             self.FILEDOC.PATH, "line {:d}".format(self.row),
>         )
>         raise RuntimeError
>     else:
>         pass
>     given, hint = argdoc.items[num]
>     num += 1
>
>     # Argument name should match given definition.
>     if (name == given):
>         pass
>     else:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " defined argument \"{:s}\" does not match described" \
>             " argument name \"{:s}\".",
>             self.FILEDOC.PATH, "line {:d}".format(self.row),
>             given, name,
>         )
>         raise RuntimeError
>     self.arg_names.append(name)
>     self.arg_hints.append(hint.text())
>
>     # Some arguments have no attachment.
>     if (name in ("self", "cls", "*args", "**kargs")):
>         self.arg_descs.append([])
>         continue
>     else:
>         pass
>
>     # Get attachment.
>     buf = []
>     while (ptr < len(texts)):
>         if (texts[ptr][0].isspace()):
>             pass
>         else:
>             break
>         buf.append(texts[ptr][UNIT:])
>         ptr += 1
>     try:
>         attach = paragraphize(buf)
>     except:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " fail to translate paragraphs.",
>             self.FILEDOC.PATH, "line {:d}".format(self.row),
>         )
>         raise RuntimeError
>     self.arg_descs.append(attach)
> del self.texts_args
>
> # Check if there is argument without description.
> if (num == len(argdoc.items)):
>     pass
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " some defined arguments (\"{:s}\", ...)have no descriptions.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>         argdoc.items[num][0],
>     )
>     raise RuntimeError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfuncdescdocument)

---

### Function: doc.main.FuncDescDocument.review\_returns

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3674)

Review argument and return.

> **Arguments**
> - *self*: `FuncDescDocument`
>
> - *returndoc*: `TypeHintDocument`
>
>   Return document.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Get texts.
> texts = self.texts_returns
>
> # Argument description has constant head.
> if (texts[0] == "Returns" and texts[1] == "-------"):
>     pass
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " return document has constant head.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
>
> # Decode return document into a list a return type hints.
> if (returndoc.name == "None"):
>     returnlist = []
> elif (returndoc.name == "MultiReturn"):
>     returnlist = returndoc.children
> else:
>     returnlist = [returndoc]
>
> # Traverse later contents.
> ptr = 0
> texts = texts[2:]
> num = 0
> self.return_names = []
> self.return_hints = []
> self.return_descs = []
> while (ptr < len(texts)):
>     # Get argument name.
>     name = texts[ptr][2:]
>     ptr += 1
>
>     # Get definition.
>     if (num == len(returnlist)):
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " defined returns are less than described returns.",
>             self.FILEDOC.PATH, "line {:d}".format(self.row),
>         )
>         raise RuntimeError
>     else:
>         pass
>     hint = returnlist[num]
>     num += 1
>     self.return_names.append(name)
>     self.return_hints.append(hint.text())
>
>     # Get attachment.
>     buf = []
>     while (ptr < len(texts)):
>         if (texts[ptr][0].isspace()):
>             pass
>         else:
>             break
>         buf.append(texts[ptr][UNIT:])
>         ptr += 1
>     try:
>         attach = paragraphize(buf)
>     except:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " fail to translate paragraphs.",
>             self.FILEDOC.PATH, "line {:d}".format(self.row),
>         )
>         raise RuntimeError
>     self.return_descs.append(attach)
> del self.texts_returns
>
> # Check if there is argument without description.
> if (num == len(returnlist)):
>     pass
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " some defined returns have no descriptions.",
>         self.FILEDOC.PATH, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy) [[Class]](#class-docmainfuncdescdocument)

## Section: Main

Main branch starts from here.

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## Block: doc.main: Main branch.

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/main.py#L3785)

> ```python
> # Main branch.
> if (__name__ == "__main__"):
>     # Generate all notes.
>     doc = DirectoryDocument(os.path.abspath("."), rootdoc=None)
>     doc.parse()
> else:
>     pass
> ```

[[TOC]](#table-of-content) [[File]](#file-docmainpy)

---

## File: doc/code.py

* [Section: Code Objects](#section-code-objects)
  * [Class: doc.code.Word](#class-doccodeword)
    * [Function: doc.code.Word.set](#function-doccodewordset)
    * [Function: doc.code.Word.position](#function-doccodewordposition)
    * [Function: doc.code.Word.check](#function-doccodewordcheck)
  * [Class: doc.code.Line](#class-doccodeline)
    * [Function: doc.code.Line.set](#function-doccodelineset)
    * [Function: doc.code.Line.append](#function-doccodelineappend)
    * [Function: doc.code.Line.reset](#function-doccodelinereset)
    * [Function: doc.code.Line.check](#function-doccodelinecheck)
    * [Function: doc.code.Line.match](#function-doccodelinematch)
    * [Function: doc.code.Line.get](#function-doccodelineget)
    * [Function: doc.code.Line.next](#function-doccodelinenext)
    * [Function: doc.code.Line.eol](#function-doccodelineeol)
  * [Block: doc.code: Define essential...](#block-doccode-define-essential)
  * [Block: doc.code: Define single wor...](#block-doccode-define-single-wor)
  * [Block: doc.code: Overwrite compose...](#block-doccode-overwrite-compose)
  * [Block: doc.code: Define not-word w...](#block-doccode-define-not-word-w)
  * [Block: doc.code: Define sentence w...](#block-doccode-define-sentence-w)
  * [Block: doc.code: Define sentence r...](#block-doccode-define-sentence-r)
  * [Class: doc.code.Code](#class-doccodecode)
    * [Function: doc.code.Code.\_\_init\_\_](#function-doccodecode__init__)
    * [Function: doc.code.Code.load\_file](#function-doccodecodeload_file)
    * [Function: doc.code.Code.load\_texts](#function-doccodecodeload_texts)
    * [Function: doc.code.Code.load\_tokens](#function-doccodecodeload_tokens)
    * [Function: doc.code.Code.rule\_texts](#function-doccodecoderule_texts)
    * [Function: doc.code.Code.review](#function-doccodecodereview)
    * [Function: doc.code.Code.clear\_space\_until](#function-doccodecodeclear_space_until)
    * [Function: doc.code.Code.clear\_string](#function-doccodecodeclear_string)
    * [Function: doc.code.Code.clear\_common](#function-doccodecodeclear_common)
    * [Function: doc.code.Code.recoverable](#function-doccodecoderecoverable)
    * [Function: doc.code.Code.reset](#function-doccodecodereset)
    * [Function: doc.code.Code.get](#function-doccodecodeget)
    * [Function: doc.code.Code.next](#function-doccodecodenext)
    * [Function: doc.code.Code.eof](#function-doccodecodeeof)
    * [Function: doc.code.Code.blank\_top](#function-doccodecodeblank_top)
    * [Function: doc.code.Code.blank\_next](#function-doccodecodeblank_next)
  * [Function: doc.code.line\_rule\_length](#function-doccodeline_rule_length)
  * [Function: doc.code.line\_rule\_char](#function-doccodeline_rule_char)
  * [Function: doc.code.line\_rule\_break](#function-doccodeline_rule_break)
  * [Function: doc.code.recover](#function-doccoderecover)
  * [Function: doc.code.paragraphize](#function-doccodeparagraphize)
  * [Function: doc.code.mathize](#function-doccodemathize)
  * [Function: doc.code.codize](#function-doccodecodize)
  * [Function: doc.code.textize](#function-doccodetextize)

## Section: Code Objects

Tokenized code for any arbitrary file is defined based on Python token library. Each tokenized code word is automatically attached with its indent level for later styled document check.

Style related constants and utility functions are also defined.

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Class: doc.code.Word

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L44)

- Super: object

Token word.

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

- Members:
  * [Function: doc.code.Word.set](#function-doccodewordset)
  * [Function: doc.code.Word.position](#function-doccodewordposition)
  * [Function: doc.code.Word.check](#function-doccodewordcheck)

---

### Function: doc.code.Word.set

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L48)

Set word attributes.

> **Arguments**
> - *self*: `Word`
>
> - *\*args*: `object`
>
> - *val*: `int`
>
>   Token integer.
>
> - *text*: `str`
>
>   Token text content.
>
> - *row*: `int`
>
>   Token row index.
>
> - *column*: `int`
>
>   Token column index.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Save necessary attributes.
> self.token = val
> self.token_string = token.tok_name[self.token]
> self.text = text
> self.row = row
> self.column = column
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeword)

---

### Function: doc.code.Word.position

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L80)

Get position string.

> **Arguments**
> - *self*: `Word`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *msg*: `str`
>
>   Position string.

> ```python
> # Get indent level, line (row) and column.
> return "line {:d}, column: {:d}".format(self.row, self.column)
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeword)

---

### Function: doc.code.Word.check

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L99)

Check given arguments with memory.

> **Arguments**
> - *self*: `Word`
>
> - *target*: `Union[int, str]`
>
>   Target.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   If True, the target is satisfied by scanning memory.

> ```python
> # Check attribute according to target type.
> if (isinstance(target, int)):
>     return self.token == target
> else:
>     return self.text == target
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeword)

---

## Class: doc.code.Line

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L126)

- Super: object

Line of tokens.

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

- Members:
  * [Function: doc.code.Line.set](#function-doccodelineset)
  * [Function: doc.code.Line.append](#function-doccodelineappend)
  * [Function: doc.code.Line.reset](#function-doccodelinereset)
  * [Function: doc.code.Line.check](#function-doccodelinecheck)
  * [Function: doc.code.Line.match](#function-doccodelinematch)
  * [Function: doc.code.Line.get](#function-doccodelineget)
  * [Function: doc.code.Line.next](#function-doccodelinenext)
  * [Function: doc.code.Line.eol](#function-doccodelineeol)

---

### Function: doc.code.Line.set

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L130)

Set line attributes.

> **Arguments**
> - *self*: `Line`
>
> - *\*args*: `object`
>
> - *level*: `int`
>
>   Indent level.
>
> - *text*: `str`
>
>   Raw code text.
>
> - *path*: `str`
>
>   Path to the file of the line.
>
> - *row*: `int`
>
>   Line row ID in the file of the line.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Save necessary attributes.
> self.level = level
> self.implicit = False
> self.text = text
> self.path = path
> self.row = row
> self.memory: List[Word] = []
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeline)

---

### Function: doc.code.Line.append

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L163)

Append a word starting from the line.

> **Arguments**
> - *self*: `Line`
>
> - *word*: `Word`
>
>   Appending word.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Append directly
> self.memory.append(word)
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeline)

---

### Function: doc.code.Line.reset

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L182)

Reset scanning status.

> **Arguments**
> - *self*: `Line`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Reset scanning pointer.
> self.scan = 0
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeline)

---

### Function: doc.code.Line.check

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L199)

Check given arguments with memory.

> **Arguments**
> - *self*: `Line`
>
> - *target*: `Union[int, str]`
>
>   Target.
>
> - *\*args*: `object`
>
> - *level*: `int`
>
>   Required indent level.
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   If True, the target is satisfied by scanning memory.

> ```python
> # Check indent level.
> if (self.level != level):
>     return False
> else:
>     pass
>
> # Check scanning word.
> return self.get().check(target)
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeline)

---

### Function: doc.code.Line.match

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L231)

Match given arguments with memory.

> **Arguments**
> - *self*: `Line`
>
> - *target*: `Union[int, str]`
>
>   Target.
>
> - *\*args*: `object`
>
> - *level*: `int`
>
>   Required indent level.
>
> - *\*\*kargs*: `object`

> **Returns**

It is a more strict version of check function that target must be satisfied. Otherwise, runtime error will be reported.

> ```python
> # Check indent level.
> if (self.level != level):
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " wrong indent level.",
>         self.path, "line {:d}".format(self.row),
>     )
>     raise RuntimeError
> else:
>     pass
>
> # Match scanning.
> obj = self.get()
> if (obj.check(target)):
>     pass
> elif (isinstance(target, int)):
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " expect {:s}, but get {:s}.",
>         self.path, obj.position(),
>         token.tok_name[target], obj.token_string,
>     )
>     raise RuntimeError
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " expect \"{:s}\", but get \"{:s}\".",
>         self.path, obj.position(),
>         repr(target)[1:-1], repr(obj.text)[1:-1],
>     )
>     raise RuntimeError
>
> # Move to next if match successfully.
> self.next()
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeline)

---

### Function: doc.code.Line.get

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L290)

Get scanning word.

> **Arguments**
> - *self*: `Line`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *word*: `Word`
>
>   Scanning word.

> ```python
> # Get directly.
> return self.memory[self.scan]
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeline)

---

### Function: doc.code.Line.next

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L309)

Move pointer to next word.

> **Arguments**
> - *self*: `Line`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Move to next non-trivial pointer.
> self.scan += 1
> while (not self.eol() and self.get().token == token.INDENT):
>     self.scan += 1
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeline)

---

### Function: doc.code.Line.eol

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L328)

Get EOL signal.

> **Arguments**
> - *self*: `Line`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   Signal for EOL.

> ```python
> # Get directly.
> return self.scan == len(self.memory)
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodeline)

---

## Block: doc.code: Define essential...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L348)

> ```python
> # Define essential constants.
> UNIT = 4
> MAX = 79
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Block: doc.code: Define single wor...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L353)

> ```python
> # Define single word regex.
> NUMBER = r"[1-9][0-9]*"
> INITIAL = r"([A-Z][A-Za-z]*|{:s})".format(NUMBER)
> INSIDE = r"([A-Za-z]+|{:s})".format(NUMBER)
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Block: doc.code: Overwrite compose...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L359)

> ```python
> # Overwrite composed word regex.
> INITIAL = r"({:s}(-{:s})*)".format(INITIAL, INSIDE)
> INSIDE = r"({:s}(-{:s})*)".format(INSIDE, INSIDE)
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Block: doc.code: Define not-word w...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L364)

> ```python
> # Define not-word word regex.
> MATH = r"\$([^\n\\\$]|\\[^\n])+\$"
> CODE = r"`([^\n\\`]|\\[^\n])+`"
> STRING = r"\"([^\n\\\"]|\\[^\n])+\""
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Block: doc.code: Define sentence w...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L370)

> ```python
> # Define sentence word regex.
> FIRST = r"({:s}|{:s}|{:s}|{:s})".format(INITIAL, MATH, CODE, STRING)
> LATER = r"({:s}|{:s}|{:s}|{:s})".format(INSIDE, MATH, CODE, STRING)
> BREAK = r"( |, )"
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Block: doc.code: Define sentence r...

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L376)

> ```python
> # Define sentence regex.
> PARANTHESE = r"\({:s}({:s}{:s})*\)".format(LATER, BREAK, LATER)
> SENTENCE = r"^{:s}({:s}{:s}({:s}{:s})?)*.$".format(
>     FIRST, BREAK, LATER, BREAK, PARANTHESE,
> )
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Class: doc.code.Code

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L383)

- Super: object

Tokenized code with indent of a file.

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

- Members:
  * [Function: doc.code.Code.\_\_init\_\_](#function-doccodecode__init__)
  * [Function: doc.code.Code.load\_file](#function-doccodecodeload_file)
  * [Function: doc.code.Code.load\_texts](#function-doccodecodeload_texts)
  * [Function: doc.code.Code.load\_tokens](#function-doccodecodeload_tokens)
  * [Function: doc.code.Code.rule\_texts](#function-doccodecoderule_texts)
  * [Function: doc.code.Code.review](#function-doccodecodereview)
  * [Function: doc.code.Code.clear\_space\_until](#function-doccodecodeclear_space_until)
  * [Function: doc.code.Code.clear\_string](#function-doccodecodeclear_string)
  * [Function: doc.code.Code.clear\_common](#function-doccodecodeclear_common)
  * [Function: doc.code.Code.recoverable](#function-doccodecoderecoverable)
  * [Function: doc.code.Code.reset](#function-doccodecodereset)
  * [Function: doc.code.Code.get](#function-doccodecodeget)
  * [Function: doc.code.Code.next](#function-doccodecodenext)
  * [Function: doc.code.Code.eof](#function-doccodecodeeof)
  * [Function: doc.code.Code.blank\_top](#function-doccodecodeblank_top)
  * [Function: doc.code.Code.blank\_next](#function-doccodecodeblank_next)

---

### Function: doc.code.Code.\_\_init\_\_

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L387)

Initialize.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Nothing is requires.
> pass
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.load\_file

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L404)

Load code tokens from given file.

> **Arguments**
> - *self*: `Code`
>
> - *path*: `str`
>
>   File path.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Save loaded path.
> self.path = path
>
> # Load file text lines.
> self.load_texts()
> self.rule_texts()
>
> # Load file tokens.
> self.load_tokens()
>
> # Review text lines and file tokens as lines of tokens.
> self.review()
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.load\_texts

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L435)

Load text lines from given file.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Read text lines along with indent level.
> self.texts = []
> file = open(self.path, "r")
> eof = False
> for i, line in enumerate(file):
>     # Should not read in anything after EOF.
>     if (eof):
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " read after EOF (line w.o. tail \"\\n\").",
>             self.path, "line {:d}".format(i + 1),
>         )
>         raise RuntimeError
>     else:
>         pass
>
>     # Exclude tail spaces except for "\n".
>     rclean = line.rstrip()
>     if (len(rclean) == len(line)):
>         # Only the last line should have no "\n".
>         eof = True
>     elif (len(rclean) + 1 == len(line) and line[-1] == "\n"):
>         pass
>     else:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " find tail spaces.",
>             self.path, "line {:d}".format(i + 1),
>         )
>         raise RuntimeError
>
>     # Numer of spaces must fit the unit.
>     lclean = rclean.lstrip()
>     num_spaces = len(rclean) - len(lclean)
>     if (num_spaces % UNIT == 0):
>         level = num_spaces // UNIT
>     else:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " weird indent.",
>             self.path, "line {:d}".format(i + 1),
>         )
>         raise RuntimeError
>
>     # Blank line is special.
>     if (len(lclean) == 0):
>         self.texts.append((-1, rclean))
>     else:
>         self.texts.append((level, rclean))
> file.close()
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.load\_tokens

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L500)

Load tokens from given file.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Load tokens except indent or dedent.
> self.tokens = []
> file = open(self.path, "r")
> buf = tokenize.generate_tokens(file.readline)
> for itr in buf:
>     if (itr[0] in (token.INDENT, token.DEDENT)):
>         # Indent token is modified for other usage.
>         pass
>     else:
>         self.tokens.append(itr)
> file.close()
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.rule\_texts

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L526)

Check rules over text lines.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Check each text lines.
> for i, (_, text) in enumerate(self.texts):
>     line_rule_length(text=text, index=i + 1, path=self.path)
>     line_rule_char(text=text, index=i + 1, path=self.path)
>     line_rule_break(text=text, index=i + 1, path=self.path)
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.review

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L546)

Review text lines and tokens as lines of tokens.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Define real buffer.
> self.memory = []
> self.ptrs = []
> for i, (level, text) in enumerate(self.texts):
>     line = Line()
>     line.set(level=level, text=text, path=self.path, row=i + 1)
>     self.memory.append(line)
>     self.ptrs.append(0)
> del self.texts
>
> # Traverse tokens and put to corresponding lines.
> scan = 0
> while (scan < len(self.tokens) - 1):
>     # Get the starting token.
>     val, text, head, tail, _ = self.tokens[scan]
>     head_row, head_col = head
>     tail_row, tail_col = tail
>     scan += 1
>
>     # Get the space ahead.
>     self.clear_space_until(head_row, head_col)
>
>     # Create word.
>     word = Word()
>     word.set(val=val, text=text, row=head_row, column=head_col)
>
>     # Update line pointer in memory.
>     if (val == token.STRING):
>         # Update string token (multiple-line or not).
>         self.clear_string(word)
>     elif (head_row == tail_row):
>         # Update single-line token.
>         self.clear_common(word)
>     else:
>         error(
>             "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>             " only string allows multiple-line code.",
>             self.path,
>             "line {:d}, column: {:d}".format(head_row, head_col),
>         )
>         raise RuntimeError
> del self.tokens
> del self.ptrs
>
> # Ensure that multiple-line string only involves in definition.
> for itr in self.memory:
>     if (itr.implicit and len(itr.memory) > 0):
>         if (
>             len(itr.memory) == 1 and itr.memory[0].check(token.NEWLINE)
>         ):
>             pass
>         else:
>             error(
>                 "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>                 " Only end of statement can be multiple-line string.",
>                 self.path, "line {:d}".format(itr.row),
>             )
>             raise RuntimeError
>     else:
>         pass
>
> # Ensure raw code is recoverable.
> self.recoverable()
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.clear\_space\_until

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L624)

Clear space at given row from pointer until given column.

> **Arguments**
> - *self*: `Code`
>
> - *row*: `int`
>
>   Given row.
>
> - *column*: `int`
>
>   Given column (exclusive).
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Get information of given row.
> row -= 1
> obj = self.memory[row]
> buf = obj.memory
> line = obj.text
> ptr = self.ptrs[row]
> length = column - ptr
>
> # Update memory.
> if (length == 0):
>     # No-space case should be ignored.
>     pass
> elif (len(buf) == 0):
>     # Spaces of line indent should be ignored.
>     pass
> elif (length != 1):
>     # Space break can at most have 1 space.
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " space break can at most have 1 space.",
>         self.path,
>         "line {:d}, column: {:d}".format(row + 1, ptr),
>     )
>     raise RuntimeError
> else:
>     # Use None to represent single-space break token.
>     word = Word()
>     word.set(val=token.INDENT, text=" ", row=row + 1, column=ptr)
>     buf.append(word)
>
> # Update pointer.
> self.ptrs[row] += length
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.clear\_string

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L677)

Clear and update a possibly multiple-line string token.

> **Arguments**
> - *self*: `Code`
>
> - *word*: `Word`
>
>   Word token.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Get information of the word.
> row = word.row - 1
> texts = word.text.split("\n")
> num_lines = len(texts)
>
> # Update memory.
> self.memory[row].append(word)
> for i in range(1, num_lines):
>     # Mark as not existing except for the first line.
>     if (i > 0):
>         self.memory[row + i].implicit = True
>     else:
>         pass
>
> # Update pointer.
> for i, text in enumerate(texts):
>     self.ptrs[row + i] += len(text)
>
> # Tail "\\" after string means a concatenation.
> focus = row + num_lines - 1
> ptr = self.ptrs[focus]
> if (self.memory[focus].text[ptr:] == " \\"):
>     # Create extra NL word.
>     word = Word()
>     word.set(val=token.NL, text=" \\\n", row=focus + 1, column=ptr)
>     self.memory[focus].append(word)
> else:
>     pass
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.clear\_common

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L724)

Clear and update a single-line token.

> **Arguments**
> - *self*: `Code`
>
> - *word*: `Word`
>
>   Word token.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Get information of the word.
> row = word.row - 1
> length = len(word.text)
>
> # Update memory.
> self.memory[row].append(word)
>
> # Update pointer.
> self.ptrs[row] += length
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.recoverable

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L752)

Ensure raw code to be recoverable.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Traverse the memory.
> ptr = 0
> while (ptr < len(self.memory)):
>     # Get tokens and raw codes.
>     tokens = []
>     raws = []
>     position = ptr + 1
>     obj = self.memory[ptr]
>     level = obj.level
>     tokens.extend(obj.memory)
>     raws.append(obj.text)
>     ptr += 1
>     while (ptr < len(self.memory) and self.memory[ptr].implicit):
>         obj = self.memory[ptr]
>         tokens.extend(obj.memory)
>         raws.append(obj.text)
>         ptr += 1
>
>     # Generate by tokens
>     texts = [" " * level * UNIT]
>     for word in tokens:
>         if (word is None):
>             texts.append(" ")
>         else:
>             texts.append(word.text)
>     generates = "".join(texts).split("\n")
>
>     # Remove trivial generation tail.
>     if (len(generates[-1]) == 0):
>         del generates[-1]
>     else:
>         pass
>
>     # Ensure matching.
>     for i in range(max(len(raws), len(generates))):
>         if (raws[i] != generates[i]):
>             error(
>                 "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>                 " fail to recover code.",
>                 self.path, "line {:d}".format(position + i),
>             )
>             raise RuntimeError
>         else:
>             pass
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.reset

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L811)

Reset scanning status.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Reset scanning pointer.
> self.scan = 0
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.get

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L828)

Get scanning line.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *line*: `Line`
>
>   Scanning line.

> ```python
> # Get directly.
> return self.memory[self.scan]
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.next

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L847)

Move pointer to next line.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Move directly.
> self.scan += 1
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.eof

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L864)

Get EOF signal.

> **Arguments**
> - *self*: `Code`
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   Signal for EOF.

> ```python
> # Get directly.
> return self.scan == len(self.memory)
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.blank\_top

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L883)

Get blank line signal.

> **Arguments**
> - *self*: `Code`
>
> - *num*: `int`
>
>   Number of blank lines.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *flag*: `bool`
>
>   Signal for single blank line.

> ```python
> # Fetch lines and check if they are all blank.
> for i in range(num):
>     # EOF is equivalent to any number of blank lines.
>     if (self.scan + i == len(self.memory)):
>         break
>     else:
>         pass
>
>     # Fetch line and check.
>     obj = self.memory[self.scan + i]
>     if (len(obj.memory) == 1 and obj.memory[0].check(token.NL)):
>         pass
>     else:
>         return False
> return True
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

### Function: doc.code.Code.blank\_next

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L919)

Get blank line and skip.

> **Arguments**
> - *self*: `Code`
>
> - *num*: `int`
>
>   Number of blank lines.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Check and skip.
> if (self.blank_top(num)):
>     for i in range(num):
>         if (self.eof()):
>             break
>         else:
>             self.next()
> else:
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " expect {:d} blank lines.",
>         self.path, "line {:d}".format(self.get().row), num,
>     )
>     raise RuntimeError
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy) [[Class]](#class-doccodecode)

---

## Function: doc.code.line\_rule\_length

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L953)

Check length rule over a text line.

> **Arguments**
> - *text*: `str`
>
>   Line content.
>
> - *\*args*: `object`
>
> - *index*: `int`
>
>   Line index.
>
> - *path*: `str`
>
>   File path.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Text length is limited.
> if (len(text) > MAX):
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " too long (>{:d}).",
>         path, "line {:d}".format(index),
>         MAX,
>     )
>     raise RuntimeError
> else:
>     pass
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Function: doc.code.line\_rule\_char

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L987)

Check character rule over a text line.

> **Arguments**
> - *text*: `str`
>
>   Line content.
>
> - *\*args*: `object`
>
> - *index*: `int`
>
>   Line index.
>
> - *path*: `str`
>
>   File path.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Some charaters are rejected.
> if (chr(39) in text):
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " invalid char \"{:s}\".",
>         path, "line {:d}".format(index),
>         chr(39),
>     )
>     raise RuntimeError
> else:
>     pass
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Function: doc.code.line\_rule\_break

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1021)

Check line break rule over a text line.

> **Arguments**
> - *text*: `str`
>
>   Line content.
>
> - *\*args*: `object`
>
> - *index*: `int`
>
>   Line index.
>
> - *path*: `str`
>
>   File path.
>
> - *\*\*kargs*: `object`

> **Returns**

> ```python
> # Line break is rejected except for strings.
> if (text[-2:] == " \\" and text[-3] != "\""):
>     error(
>         "At \"{:s}\", \033[31;1;47;1m{:s}\033[0m," \
>         " line break is disabled.",
>         path, "line {:s}".format(index),
>     )
>     raise RuntimeError
> else:
>     pass
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Function: doc.code.recover

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1054)

Recover code from given memory of tokens.

> **Arguments**
> - *memory*: `List[Word]`
>
>   Memory of tokens.
>
> - *\*args*: `object`
>
> - *level*: `int`
>
>   Indent level.
>
> - *\*\*kargs*: `object`

> **Returns**
> - *texts*: `List[str]`
>
>   A list of generated code lines.

> ```python
> # Generate directly
> texts = [" " * level * UNIT]
> for word in memory:
>     texts.append(word.text)
> return "".join(texts).split("\n")
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Function: doc.code.paragraphize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1082)

Transfer a list of texts into paragraphs.

> **Arguments**
> - *texts*: `List[str]`
>
>   Texts.
>
> - *\*args*: `object`
>
> - *\*\*kargs*: `object`

> **Returns**
> - *paragraphs*: `List[List[str]]`
>
>   Paragraphs.

> ```python
> # Empty is a special case.
> if (len(texts) == 0):
>     return []
> else:
>     pass
>
> # Attach an additional blank line as replace of EOP.
> buf = texts + [""]
>
> # Break texts by single blank line.
> ptr = 0
> paragraphs = []
> while (ptr < len(buf)):
>     # Reject empty paragraph.
>     if (len(buf[ptr]) == 0):
>         error(
>             "At comment line {:d}, empty paragraph is rejected.",
>             ptr + 1,
>         )
>         raise RuntimeError
>     else:
>         pass
>
>     # Take lines for decoding until a blank line.
>     start = ptr
>     decoding = []
>     while (len(buf[ptr]) > 0):
>         decoding.append(buf[ptr])
>         ptr += 1
>
>     # Decode according to different flags.
>     if (decoding[0] == "$$"):
>         paragraphs.extend(mathize(decoding, start=start + 1))
>     elif (decoding[0][0:3] == "```"):
>         paragraphs.extend(codize(decoding, start=start + 1))
>     else:
>         paragraphs.extend(textize(decoding, start=start + 1))
>
>     # Go over the blank line to move to next.
>     ptr += 1
> return paragraphs
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Function: doc.code.mathize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1144)

Transfer a list of texts into math block.

> **Arguments**
> - *texts*: `List[str]`
>
>   Texts.
>
> - *\*args*: `object`
>
> - *start*: `int`
>
>   Starting line in original text.
>
> - *\*\*kargs*: `object`

> **Returns**
> - *block*: `List[List[str]]`
>
>   Math block.

> ```python
> # Block must end properly.
> if (texts[-1] != "$$"):
>     error(
>         "At comment line {:d}, multiple-line math starts from" \
>         " line {:d} but ends nowhere.",
>         start + len(texts) - 1, start,
>     )
>     raise RuntimeError
> else:
>     pass
>
> # Math block requires no decoding.
> return [[itr] for itr in texts]
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Function: doc.code.codize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1180)

Transfer a list of texts into code block.

> **Arguments**
> - *texts*: `List[str]`
>
>   Texts.
>
> - *\*args*: `object`
>
> - *start*: `int`
>
>   Starting line in original text.
>
> - *\*\*kargs*: `object`

> **Returns**
> - *block*: `List[List[str]]`
>
>   Math block.

> ```python
> # Block must end properly.
> if (texts[-1] != "```"):
>     error(
>         "At comment line {:d}, multiple-line code starts from" \
>         " line {:d} but ends nowhere.",
>         start + len(texts) - 1, start,
>     )
>     raise RuntimeError
> else:
>     pass
>
> # Math block requires no decoding.
> return [[itr] for itr in texts]
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)

---

## Function: doc.code.textize

- Source: [Github](https://github.com/gao462/MLRepo/blob/master/doc/code.py#L1216)

Transfer a list of texts into text block.

> **Arguments**
> - *texts*: `List[str]`
>
>   Texts.
>
> - *\*args*: `object`
>
> - *start*: `int`
>
>   Starting line in original text.
>
> - *\*\*kargs*: `object`

> **Returns**
> - *block*: `List[List[str]]`
>
>   Math block.

> ```python
> # Allocate buffer.
> block = []
> buf = []
>
> # Decode all text in order.
> for i, itr in enumerate(texts):
>     buf.append(itr)
>     if (itr[-1] == "." or i == len(texts) - 1):
>         # A sentence is ending, decode it and clear buffer.
>         sentence = " ".join(buf)
>         buf.clear()
>
>         # Check sentence regex.
>         if (re.match(SENTENCE, sentence) is None):
>             error(
>                 "At comment line {:d}, wrong senetence regex.\n" \
>                 "\"\"\"\n{:s}\n\"\"\".",
>                 start + i, sentence,
>             )
>             raise RuntimeError
>         else:
>             pass
>
>         # Append sentence to the block.
>         block.append(sentence)
>     else:
>         # A sentence is not ending, continue.
>         pass
> return [block]
> ```

[[TOC]](#table-of-content) [[File]](#file-doccodepy)
// Copyright (c) 2026 Ilya Snegov (aka Sierra Arn)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// composizioni/paratext/lib.typ

#import "01-title-page.typ": title-page
#import "02-copyright-page.typ": copyright-page

#let meta = toml("../../metadata.toml")

#let paratext(
    number: none,
    title: none,
    instruments: none,
    author: meta.author.display_name,
    legal-name: meta.author.legal_name,
    collection: meta.work.collection,
) = {
    set page(
        paper: "a4",
        margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    )

    set text(
        font: "Libertinus Serif",
        size: 12pt,
        lang: "en",
    )

    let date = datetime(
        year: meta.date.year,
        month: meta.date.month,
        day: meta.date.day,
    )

    set document(
        title: [No. #number: #title],
        author: author,
        date: date,
    )

    title-page(
        collection: collection,
        number: number,
        title: title,
        instruments: instruments,
        author: author,
        date: date,
    )

    copyright-page(
        year: date.year(),
        author: author,
        legal-name: legal-name,
        email: meta.author.email,
        license-name: meta.license.name,
        license-designation: meta.license.designation,
        license-url: meta.license.url,
    )
}

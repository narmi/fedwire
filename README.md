# fedwire
[![Build Status](https://travis-ci.org/narmitech/fedwire.svg?branch=master)](https://travis-ci.org/narmitech/fedwire)

A python package that implements an interface to write files for the [Fedwire Funds Service](https://www.frbservices.org/financial-services/wires/index.html), [a real-time gross settlement funds transfer system operated by the United States Federal Reserve Banks](https://en.wikipedia.org/wiki/Fedwire). These [compatible files](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.445.7645&rep=rep1&type=pdf) include routing instructions that, once received and processed, will debit the funds from the sending bank's reserve account at their Federal Reserve bank and credit the receiving bank's account. Wire transfers sent via Fedwire are completed in the same day, while some are completed instantly.

## Usage

```
from datetime import datetime
from decimal import Decimal

from fedwire import FedwireFile, Entry, Tag

wire_file = FedwireFile()
entries = [
    Entry([
      Tag.sender_supplied_information(production=True),
      Tag.type(Tag.TYPE_FUNDS_TRANSFER, TAG.SUBTYPE_BASIC_FUNDS_TRANSFER),
      Tag.imad(datetime.now(), source, sequence),
      Tag.amount(Decimal('123')),
      Tag.sender_institution(routing, name),
      Tag.receiver_institution(routing, name),
      Tag.business_function_code(business, transaction),
    ])
]
wire_file.add_batch(entries)
print(wire_file)
```

## Format details

The Fedwire Funds Service message format consists of tags and data elements within those tags. Elements are either fixed or variable in length, with a maximum number of characters allotted for each element.

## License

Apache License 2.0 See LICENSE for details.

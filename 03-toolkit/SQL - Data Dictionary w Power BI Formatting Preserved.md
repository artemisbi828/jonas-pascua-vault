- + char(13) + char(10) + --> spaces between bullets
- + char(13) + char(10) + char(13) + char(10) + --> spaces after paragraphs
```sql
           ('Net Collections', N'Collections less refunds and reversals.'),
           ('Average Case Fee',
            N'Net production divided by total case starts (excludes add-on only contracts).' + char(13) + char(10) + char(13) + char(10)
            + N'- To improve average case fee, limit discounts, maximize in-network plans by itemizing applicable services, and add smile enhancements (add-ons).' + char(13) + char(10)
            + N'- To view average case fee by treatment plan group go to the Trending Performance Production Dashboard and filter under Treatment Group.' + char(13) + char(10)
            + N'- Example: Filter to Full Treatment Braces and Full Treatment Invisalign to view only Full Treatment Average Case Fee.'
    ),
```
# Week 2 — Distributed Tracing

### AWS X-Ray

This service completely sucks. I cannom make it working preoper way.

1. UI mess. I could found X-Ray group in new console. After 10 minutes.

2. This group actually did nothing. I counld't filter events based on `service("backend-flask")`. No, the name was correct.

3. Custom segment/subsegment did now work also. Copy-paste example threw the exception `SegmentNotFoundException: cannot find the current segment/subsegment, please make sure you have a segment open` althought segment should start
```python
# Start a segment
segment = xray_recorder.begin_segment('segment_name')
# Start a subsegment
subsegment = xray_recorder.begin_subsegment('subsegment_name')

# Add metadata or annotation here if necessary
segment.put_metadata('key', dict, 'namespace')
subsegment.put_annotation('key', 'value')
xray_recorder.end_subsegment()

# Close the segment
xray_recorder.end_segment()
```

4. Maybe `HomeActivities` handler was not the correct place?

5. Found another way to add custom segments.
```
document = xray_recorder.current_segment()
document.put_metadata("my key", "my value")
```

6. It worked. But how can I add custom segment?

7. Lol! I did all these steps in the middle of the appropriate video. And guess what? Andrew stuck at the same part with the same issues. Bruh. Shame on you, Amazon.

8. Double lol. In the next video Andrew shows how to fix it.

### Hondecomb

Much nicer than X-Ray, I really loved it.

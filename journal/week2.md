# Week 2 — Distributed Tracing

### AWS X-Ray

This service completely sucks. I cannot make it work proper way.

1. UI mess. I could find X-Ray group in the new console after 10 minutes.

2. This group actually did nothing. I couldn't filter events based on `service("backend-flask")`. No, the name was correct.

3. Custom segment/subsegment did now work also. Copy-paste example threw the exception `SegmentNotFoundException: cannot find the current segment/subsegment, please make sure you have a segment open` although segment should start

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

```python
document = xray_recorder.current_segment()
document.put_metadata("my key", "my value")
```

6. It worked. But how can I add a custom segment?

7. Lol! I did all these steps in the middle of the appropriate video. And guess what? Andrew had stuck at the same part with the same issues. Bruh. Shame on you, Amazon.

8. Double lol. In the following video Andrew shows how to fix it.

### Hondecomb

Much nicer than X-Ray. I really loved it.


### AWS Cloudwatch

Got some issues with the standard python logging module, mostly due to Flask.

Ended up adding a watchtower handler to the Flask logger and passing the logger to service explicitly.


### Rollbar

Confusing moment - the access token created during intro part was fake. I had to go to projects and create a new one.

Overall UI is a bit weird. Other than that, there are a lot of valuable things there.

# Test guide

The visible suite is intentionally mixed: passing tests establish ordinary behavior, while failing tests capture incident symptoms. Start with the entire suite, then run one module at a time.

```bash
pytest
pytest tests/test_document_access.py -vv
pytest tests/test_group_isolation.py -vv
pytest tests/test_search_projection.py -vv
pytest tests/test_export_authorization.py -vv
```

Test layers:

- API tests exercise URL routing, header authentication, views, serializers, services, ORM state, and response semantics.
- Projection tests call the deterministic consumer boundary directly so event order is controlled.
- Export tests split API acceptance from worker execution so queue delay can be simulated without a broker.

Suggested TDD discipline:

1. State the invariant demonstrated by a failing test.
2. Add the smallest missing regression case if the failure does not fully describe the boundary.
3. Make one production change.
4. Run the focused module, then the complete suite.
5. Repeat under PostgreSQL and Redis before declaring the incident resolved.

Do not assume a green SQLite run proves transactional or locking behavior under PostgreSQL.

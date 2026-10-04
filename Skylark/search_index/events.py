from dataclasses import dataclass

@dataclass(frozen=True)
class IndexEvent:
    document_id: str
    acl_version: int
    title: str
    allowed_subjects: list[str]

    def as_payload(self):
        return {"document_id": self.document_id, "acl_version": self.acl_version, "title": self.title, "allowed_subjects": self.allowed_subjects}

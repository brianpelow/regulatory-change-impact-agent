"""Tests for deterministic obligation extraction."""

from rcia.extract import (
    ObligationExtractor,
    classify_topics,
    find_modal,
    split_sentences,
)


def topics_of(obligations) -> set[str]:
    return {o.topic for o in obligations}


def test_detects_must() -> None:
    assert find_modal("An institution must retain records.") == ("must", True)


def test_detects_shall() -> None:
    assert find_modal("Records shall be preserved.") == ("shall", True)


def test_detects_is_required_to() -> None:
    modal, binding = find_modal("An institution is required to monitor performance.")
    assert modal == "is required to"
    assert binding is True


def test_should_is_advisory_not_binding() -> None:
    modal, binding = find_modal("An institution should periodically verify records.")
    assert modal == "should"
    assert binding is False


def test_no_modal_returns_none() -> None:
    assert find_modal("This guidance describes supervisory expectations.") is None


def test_classify_model_risk() -> None:
    assert "model_risk" in classify_topics("The model inventory must be complete.")


def test_classify_fair_lending() -> None:
    assert "fair_lending" in classify_topics("Testing for disparate impact is required.")


def test_classify_returns_multiple_topics() -> None:
    text = "Records must be retained to reconstruct each automated decision."
    topics = classify_topics(text)
    assert "record_retention" in topics
    assert "automated_decisioning" in topics


def test_classify_unrelated_returns_empty() -> None:
    assert classify_topics("The weather today is mild.") == []


def test_split_strips_list_markers() -> None:
    sentences = split_sentences("(a) An institution must act.\n- A second item here.")
    assert sentences[0].startswith("An institution")
    assert sentences[1].startswith("A second item")


def test_extractor_finds_binding_obligations(model_risk_text: str) -> None:
    obligations = ObligationExtractor().run(model_risk_text)
    assert obligations
    assert all(o.binding for o in obligations)


def test_extractor_skips_advisory_by_default() -> None:
    text = "An institution should periodically verify that model documentation is current."
    assert ObligationExtractor().run(text) == []


def test_extractor_includes_advisory_when_requested() -> None:
    text = "An institution should periodically verify that model documentation is current."
    obligations = ObligationExtractor().run(text, include_advisory=True)
    assert obligations
    assert obligations[0].binding is False


def test_extractor_skips_short_sentences() -> None:
    assert ObligationExtractor().run("Models must work.") == []


def test_extractor_skips_untyped_obligations() -> None:
    text = "The institution must submit the annual report to the appropriate office."
    assert all(o.topic for o in ObligationExtractor().run(text))


def test_obligation_ids_are_sequential(model_risk_text: str) -> None:
    obligations = ObligationExtractor().run(model_risk_text)
    ids = [o.obligation_id for o in obligations]
    assert ids == [f"OBL-{i:03d}" for i in range(1, len(ids) + 1)]


def test_extraction_is_deterministic(model_risk_text: str) -> None:
    first = ObligationExtractor().run(model_risk_text)
    second = ObligationExtractor().run(model_risk_text)
    assert [o.obligation_id for o in first] == [o.obligation_id for o in second]
    assert [o.topic for o in first] == [o.topic for o in second]


def test_duplicate_sentences_deduplicated_per_topic() -> None:
    sentence = "An institution must maintain a complete model inventory of every model."
    obligations = ObligationExtractor().run(f"{sentence}\n{sentence}")
    model_risk = [o for o in obligations if o.topic == "model_risk"]
    assert len(model_risk) == 1


def test_short_truncates_long_text() -> None:
    obligations = ObligationExtractor().run(
        "An institution must maintain a complete model inventory " + "and additional detail " * 20
    )
    assert obligations[0].short(60).endswith("...")
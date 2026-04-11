# Decision: Remove Unsupported Temperature Parameter from API Calls

## Decision
Remove the `temperature` parameter from all OpenAI API calls in `qa_service.py`. Use the API's default temperature value instead.

## Context
After UI refactoring, the app threw an API error: "temperature does not support 0.3 with this model. Only the default (1) value is supported."

The custom OpenAI models available on the user's API platform (gpt-4.1-nano-2025-04-14 and gpt-5-nano-2025-08-07) do not support the temperature parameter configuration.

## Alternatives Considered
1. **Keep temperature parameters, use different model names** - Not viable; these are the correct model names for the platform
2. **Conditionally set temperature based on model** - Over-engineered; unnecessary complexity
3. **Remove temperature parameters entirely** - ✅ CHOSEN: Simplest solution, uses API defaults

## Reasoning
- The custom models have fixed behavior (default temperature=1)
- No performance or quality loss by using defaults
- Removes API errors and simplifies code
- Cleaner, more maintainable code with fewer parameters

## Trade-offs Accepted
- Unable to control model creativity/randomness via temperature
- All completions will use the model's default temperature setting
- Models may behave differently than intended if originally tuned for specific temperature values

## Files Modified
- `services/qa_service.py` - Removed all `temperature` parameters from 6 functions

## Supersedes
N/A - first time this issue has arisen

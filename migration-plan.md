# Migration Plan: Converting Models to Pydantic

## 1. Dependencies
- Add pydantic to server-requirements.txt
- Ensure Python version is compatible (Pydantic 2.x requires Python 3.7+)

## 2. Migration Steps

### Phase 1: Update Base Infrastructure
1. Remove commons/base_model.py as it will be replaced by Pydantic's BaseModel
2. Update imports to use Pydantic's BaseModel

### Phase 2: Model Migration
Convert the following models to Pydantic:

1. **EnrollResponse** (server/models/enroll_api.py)
   - Replace BaseModel import with Pydantic
   - Convert @dataclass to Pydantic model
   - Remove custom from_dict as Pydantic handles this

2. **Event Models** (commons/events/)
   
   Calibration Events:
   - Convert ScreenSize to Pydantic model
   - Convert CalibrationEvent to Pydantic model
   - Add proper type hints for datetime field
   
   Whiteboard Events:
   - Convert PointEvent to Pydantic model
   - Convert DrawerEvent to Pydantic model
   - Convert MouseClickEvent to Pydantic model
   - Keep Enum classes as they are

3. **EnrollRequest** (server/models/enroll_api.py)
   - Convert to Pydantic model
   - Add field validation for api keys
   - Keep EnrollRole enum as is

## 3. Code Changes

### Example Pydantic Model Conversion

```python
# Before
@dataclass
class ScreenSize:
    width: int
    height: int
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ScreenSize':
        return cls(**data)

# After
from pydantic import BaseModel

class ScreenSize(BaseModel):
    width: int
    height: int
```

### Benefits of Migration
1. **Automatic Validation**: Pydantic provides runtime validation
2. **Better Type Hints**: Native support for type annotations
3. **JSON Schema**: Automatic JSON schema generation
4. **Built-in Serialization**: No need for custom to_dict/from_dict methods
5. **Documentation**: Better API documentation through generated schemas

## 4. Testing Strategy
1. Create unit tests for each converted model
2. Test serialization/deserialization
3. Test validation rules
4. Ensure backward compatibility with existing API endpoints

## 5. Migration Order
1. Add Pydantic dependency
2. Convert simple models first (ScreenSize, PointEvent)
3. Convert complex models (CalibrationEvent, DrawerEvent)
4. Convert API models (EnrollResponse, EnrollRequest)
5. Update any dependent code
6. Run tests and fix any issues

## 6. Rollback Plan
- Keep old model implementations until migration is complete
- Test thoroughly in development environment
- Have quick rollback strategy if issues arise in production
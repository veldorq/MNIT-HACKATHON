import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path.cwd()))

print("=== TESTING MODEL LOADER ===\n")

try:
    from utils.model_loader import ModelManager
    print("✓ Model loader imported successfully")
    
    # Initialize model manager
    manager = ModelManager()
    print(f"✓ ModelManager initialized")
    print(f"  Default mode: {manager.default_mode}")
    print(f"  Confidence threshold: {manager.confidence_threshold}")
    
    # Check catalog
    catalog = manager.get_catalog()
    print(f"\n✓ Available models: {len(catalog)}")
    for item in catalog:
        acc_str = f"Accuracy: {item.get('accuracy'):.4f}" if item.get('accuracy') else "Accuracy: N/A"
        print(f"  - {item['mode']:15} | {item['label']:20} | {acc_str}")
    
    # Test prediction with kaggle model
    test_text = "Scientists have discovered a new miraculous cure that doctors hate because it's too effective."
    print(f"\n=== TEST PREDICTION (kaggle) ===")
    print(f"Text: {test_text[:80]}...")
    
    result = manager.predict(test_text, mode="kaggle")
    print(f"✓ Prediction result:")
    print(f"  Prediction: {result['prediction']}")
    print(f"  Confidence: {result['confidence']:.4f}")
    print(f"  Provider: {result['provider']}")
    print(f"  Mode: {result['mode']}")
    
    # Test hybrid mode if available
    if 'hybrid' in [m['mode'] for m in catalog]:
        print(f"\n=== TEST PREDICTION (hybrid) ===")
        result_hybrid = manager.predict(test_text, mode="hybrid")
        print(f"✓ Hybrid prediction result:")
        print(f"  Prediction: {result_hybrid['prediction']}")
        print(f"  Confidence: {result_hybrid['confidence']:.4f}")
        print(f"  Provider: {result_hybrid['provider']}")
        if 'ensemble' in result_hybrid:
            print(f"  Kaggle pred: {result_hybrid['ensemble']['kaggle']['prediction']} (conf: {result_hybrid['ensemble']['kaggle']['confidence']:.4f})")
            print(f"  LIAR pred: {result_hybrid['ensemble']['liar']['prediction']} (conf: {result_hybrid['ensemble']['liar']['confidence']:.4f})")
            print(f"  Weights: {result_hybrid['ensemble']['weights']}")
    
    print("\n✓ All tests completed successfully")
    
except Exception as e:
    import traceback
    print(f"✗ ERROR: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

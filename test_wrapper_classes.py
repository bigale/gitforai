#!/usr/bin/env python3
"""
Test script for formal BeadsClient and BeadsViewerClient wrapper classes
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gitforai.integrations.beads import BeadsClient, BeadsViewerClient, BeadsConfig


def test_beads_client():
    """Test BeadsClient wrapper"""
    print("\n" + "="*70)
    print("TESTING BeadsClient WRAPPER")
    print("="*70)

    try:
        # Initialize config
        config = BeadsConfig(repo_path=Path.cwd())
        client = BeadsClient(config)

        # Test ready()
        print("\n📋 Testing ready()...")
        ready_tasks = client.ready()
        print(f"✅ Found {len(ready_tasks)} ready task(s)")

        if ready_tasks:
            print(f"   First task: {ready_tasks[0]['id']} - {ready_tasks[0]['title']}")

            # Test show()
            print(f"\n🔍 Testing show({ready_tasks[0]['id']})...")
            task = client.show(ready_tasks[0]['id'])
            print(f"✅ Retrieved task: {task['title']}")
            print(f"   Status: {task.get('status', 'N/A')}")
            print(f"   Priority: {task.get('priority', 'N/A')}")

        # Test list_all()
        print("\n📝 Testing list_all(status='open')...")
        open_tasks = client.list_all(status='open')
        print(f"✅ Found {len(open_tasks)} open task(s)")

        print("\n✅ BeadsClient: ALL TESTS PASSED")
        return True

    except Exception as e:
        print(f"\n❌ BeadsClient test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_beads_viewer_client():
    """Test BeadsViewerClient wrapper"""
    print("\n" + "="*70)
    print("TESTING BeadsViewerClient WRAPPER")
    print("="*70)

    try:
        # Initialize config
        config = BeadsConfig(repo_path=Path.cwd())
        client = BeadsViewerClient(config)

        # Test triage()
        print("\n📊 Testing triage()...")
        triage = client.triage()
        quick_ref = triage.get('triage', {}).get('quick_ref', {})
        print(f"✅ Triage successful")
        print(f"   Open: {quick_ref.get('open_count', 0)}")
        print(f"   Actionable: {quick_ref.get('actionable_count', 0)}")
        print(f"   Blocked: {quick_ref.get('blocked_count', 0)}")

        recommendations = triage.get('triage', {}).get('recommendations', [])
        if recommendations:
            top = recommendations[0]
            print(f"   Top recommendation: {top['id']} (score: {top.get('score', 0):.3f})")

        # Test insights()
        print("\n📈 Testing insights()...")
        insights = client.insights()
        metrics = insights.get('metrics', {})
        print(f"✅ Insights successful")
        print(f"   Nodes: {metrics.get('node_count', 0)}")
        print(f"   Edges: {metrics.get('edge_count', 0)}")
        print(f"   Density: {metrics.get('density', 0):.3f}")

        # Test history()
        print("\n📜 Testing history()...")
        history = client.history()
        stats = history.get('stats', {})
        print(f"✅ History successful")
        print(f"   Total issues: {stats.get('total_issues', 0)}")
        print(f"   Issues with commits: {stats.get('issues_with_commits', 0)}")

        # Test plan()
        print("\n🛤️  Testing plan()...")
        plan = client.plan()
        tracks = plan.get('tracks', [])
        print(f"✅ Plan successful")
        print(f"   Execution tracks: {len(tracks)}")

        # Test graph_export()
        print("\n🔗 Testing graph_export('json')...")
        graph = client.graph_export('json')
        print(f"✅ Graph export successful")
        if isinstance(graph, dict):
            nodes = graph.get('nodes', [])
            edges = graph.get('edges', [])
            node_count = len(nodes) if isinstance(nodes, list) else nodes if isinstance(nodes, int) else 0
            edge_count = len(edges) if isinstance(edges, list) else edges if isinstance(edges, int) else 0
            print(f"   Nodes: {node_count}")
            print(f"   Edges: {edge_count}")

        print("\n✅ BeadsViewerClient: ALL TESTS PASSED")
        return True

    except Exception as e:
        print(f"\n❌ BeadsViewerClient test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🧪 Testing Formal Beads Wrapper Classes")
    print(f"Repository: {Path.cwd()}")

    beads_client_ok = test_beads_client()
    beads_viewer_ok = test_beads_viewer_client()

    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    print(f"BeadsClient: {'✅ PASS' if beads_client_ok else '❌ FAIL'}")
    print(f"BeadsViewerClient: {'✅ PASS' if beads_viewer_ok else '❌ FAIL'}")

    if beads_client_ok and beads_viewer_ok:
        print("\n🎉 All wrapper tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())

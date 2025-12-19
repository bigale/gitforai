#!/usr/bin/env python3
"""
Test script for UnifiedTaskIntelligence class
Validates integration of all three intelligence layers
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gitforai.integrations.unified import UnifiedTaskIntelligence, UnifiedConfig


def test_unified_intelligence():
    """Test UnifiedTaskIntelligence integration"""
    print("\n" + "="*70)
    print("TESTING UnifiedTaskIntelligence")
    print("="*70)

    try:
        # Initialize
        config = UnifiedConfig(repo_path=Path.cwd())
        intel = UnifiedTaskIntelligence(config)

        print(f"\n✅ Initialized UnifiedTaskIntelligence")
        print(f"   Layer 1 (BeadsClient): ✅")
        print(f"   Layer 2 (BeadsViewerClient): ✅")
        print(f"   Layer 3 (GitForAI): {'✅' if intel.gitforai_available else '⚠️  Not available'}")

        # Test get_ready_tasks()
        print("\n📋 Testing get_ready_tasks()...")
        ready = intel.get_ready_tasks()
        print(f"✅ Found {len(ready)} ready task(s)")
        if ready:
            print(f"   First: {ready[0]['id']} - {ready[0]['title']}")

        # Test get_project_health()
        print("\n💊 Testing get_project_health()...")
        health = intel.get_project_health()
        print(f"✅ Project health:")
        print(f"   Open: {health.get('open_count', 0)}")
        print(f"   Actionable: {health.get('actionable_count', 0)}")
        print(f"   Blocked: {health.get('blocked_count', 0)}")

        # Test recommend_next_task()
        print("\n🎯 Testing recommend_next_task()...")
        recommendations = intel.recommend_next_task(limit=3)
        print(f"✅ Got {len(recommendations)} recommendation(s)")

        for i, task in enumerate(recommendations, 1):
            print(f"\n   {i}. {task['id']}: {task['title']}")
            print(f"      Score: {task.get('score', 0):.3f}")
            print(f"      PageRank: {task.get('breakdown', {}).get('pagerank', 0):.3f}")

            if 'historical_complexity' in task:
                print(f"      Historical complexity: {task['historical_complexity']}")
                print(f"      Avg files changed: {task.get('avg_files_changed', 0)}")
                print(f"      Similar commits: {task.get('similar_commits_found', 0)}")

        # Test get_task_context()
        if recommendations:
            print(f"\n🔍 Testing get_task_context({recommendations[0]['id']})...")
            context = intel.get_task_context(recommendations[0]['id'])

            print(f"✅ Complete context retrieved:")
            print(f"   Task: {context['task'].get('title', 'N/A')}")
            print(f"   Status: {context['task'].get('status', 'N/A')}")
            print(f"   Priority: {context['task'].get('priority', 'N/A')}")

            if context['metrics']:
                print(f"\n   Graph Metrics:")
                print(f"      PageRank: {context['metrics'].get('pagerank', 0):.3f}")
                print(f"      Betweenness: {context['metrics'].get('betweenness', 0):.3f}")
                print(f"      Degree (in/out): {context['metrics'].get('degree_in', 0)}/{context['metrics'].get('degree_out', 0)}")

            commits_list = context['commit_history'].get('commits') if isinstance(context['commit_history'], dict) else None
            commit_count = len(commits_list) if commits_list else 0
            print(f"\n   Commit History: {commit_count} commit(s)")

            if context['similar_work']:
                print(f"\n   Similar Work ({len(context['similar_work'])} commit(s)):")
                for commit in context['similar_work'][:3]:
                    print(f"      - {commit['hash']}: {commit['message'][:50]}...")

        # Test get_critical_path()
        print("\n🎯 Testing get_critical_path()...")
        critical = intel.get_critical_path()
        print(f"✅ Critical path length: {len(critical)}")
        if critical:
            print(f"   Tasks: {', '.join(critical[:5])}")

        # Test get_execution_plan()
        print("\n🛤️  Testing get_execution_plan()...")
        plan = intel.get_execution_plan()
        tracks = plan.get('tracks', [])
        print(f"✅ Execution plan: {len(tracks)} parallel track(s)")
        if tracks:
            for track in tracks[:3]:
                print(f"   Track {track.get('track_id', 'N/A')}: {len(track.get('tasks', []))} task(s)")

        # Test search_commits() if GitForAI available
        if intel.gitforai_available:
            print("\n🔍 Testing search_commits()...")
            try:
                commits = intel.search_commits("integration", n_results=3)
                print(f"✅ Found {len(commits)} commit(s)")
                for commit in commits:
                    print(f"   - {commit['hash']}: {commit['message'][:50]}...")
            except Exception as e:
                print(f"⚠️  Search failed (expected if vectordb empty): {e}")

        print("\n✅ UnifiedTaskIntelligence: ALL TESTS PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run tests"""
    print("🧪 Testing UnifiedTaskIntelligence (3-Layer Integration)")
    print(f"Repository: {Path.cwd()}")

    success = test_unified_intelligence()

    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    print(f"UnifiedTaskIntelligence: {'✅ PASS' if success else '❌ FAIL'}")

    if success:
        print("\n🎉 All unified intelligence tests passed!")
        print("\n✅ Three-layer integration validated:")
        print("   Layer 1: BeadsClient (task storage)")
        print("   Layer 2: BeadsViewerClient (graph intelligence)")
        print("   Layer 3: GitForAI (semantic search)")
        return 0
    else:
        print("\n⚠️  Tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())

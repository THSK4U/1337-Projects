/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:58:29 by Tsellak           #+#    #+#             */
/*   Updated: 2026/06/29 11:02:23 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	fail_take(t_dongle *dongle, t_coder *coder)
{
	queue_remove(dongle, coder);
	pthread_cond_broadcast(&dongle->cond);
	pthread_mutex_unlock(&dongle->mutex);
	return (0);
}

static int	take_one_dongle(t_coder *coder, int dongle_id)
{
	t_dongle		*dongle;
	struct timespec	ts;

	dongle = &coder->data->dongles[dongle_id];
	pthread_mutex_lock(&dongle->mutex);
	if (dongle->tail == 0 || (dongle->tail == 1 && dongle->queue[0] != coder))
		queue_push(dongle, coder);
	while (dongle->in_use || get_time_ms() < dongle->release_time
		|| dongle->queue[0] != coder)
	{
		if (get_time_ms() >= coder->deadline || simulation_check(coder->data))
			return (fail_take(dongle, coder));
		ms_to_timespec(&ts, get_next_timeout(coder, dongle));
		pthread_cond_timedwait(&dongle->cond, &dongle->mutex, &ts);
	}
	queue_pop(dongle, coder->data);
	dongle->in_use = 1;
	dongle->release_time = 0;
	pthread_cond_broadcast(&dongle->cond);
	pthread_mutex_unlock(&dongle->mutex);
	if (simulation_check(coder->data))
		return (0);
	log_action(coder, "has taken a dongle");
	return (1);
}

static void	release_one_dongle(t_coder *coder, int dongle_id)
{
	t_dongle	*dongle;

	dongle = &coder->data->dongles[dongle_id];
	pthread_mutex_lock(&dongle->mutex);
	dongle->in_use = 0;
	dongle->release_time = get_time_ms() + coder->data->dongle_cooldown;
	pthread_cond_broadcast(&dongle->cond);
	pthread_mutex_unlock(&dongle->mutex);
}

int	take_two_dongles(t_coder *coder)
{
	int	first;
	int	second;
	int	tmp;

	first = coder->left_dongle;
	second = coder->right_dongle;
	if (first == second)
		return (0);
	if (second < first)
	{
		tmp = first;
		first = second;
		second = tmp;
	}
	if (!take_one_dongle(coder, first))
		return (0);
	if (!take_one_dongle(coder, second))
	{
		release_one_dongle(coder, first);
		return (0);
	}
	return (1);
}

void	release_two_dongles(t_coder *coder)
{
	int	first;
	int	second;
	int	tmp;

	first = coder->left_dongle;
	second = coder->right_dongle;
	if (second < first)
	{
		tmp = first;
		first = second;
		second = tmp;
	}
	release_one_dongle(coder, second);
	release_one_dongle(coder, first);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 23:00:26 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/03 17:33:12 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *s)
{
	int		i;
	char	*list;

	i = ft_strlen(s);
	list = malloc(sizeof(char) * (i + 1));
	if (!list)
		return (NULL);
	i = 0;
	while (s[i])
	{
		list[i] = s[i];
		i++;
	}
	list[i] = '\0';
	return (list);
}
